from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Order
from .serializers import OrderSerializer
from products.models import Product
import razorpay
import hmac
import hashlib


# ✅ CREATE NORMAL ORDER (COD / UPI / CARD)
class CreateOrderAPIView(APIView):
    def post(self, request):
        try:
            user = request.user if request.user.is_authenticated else None
            data = request.data

            product_id = data.get("product")
            quantity = int(data.get("quantity", 1))
            address = data.get("address")
            payment_method = data.get("payment_method")
            delivery_charge = float(data.get("delivery_charge", 0))

            # 🔹 Validate required fields
            if not all([product_id, address, payment_method]):
                return Response(
                    {"error": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 🔹 Validate product existence
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # 🔹 Check stock availability
            if product.stock < quantity:
                return Response(
                    {"error": "Insufficient stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 🔹 Calculate total (backend controlled for security)
            total = (product.price * quantity) + delivery_charge

            # 🔹 Reduce stock
            product.stock -= quantity
            product.save()

            # 🔹 Delivery date (5 days from now)
            delivery_date = (timezone.now() + timedelta(days=5)).strftime("%Y-%m-%d")

            # 🔹 Create the order
            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                address=address,
                payment_method=payment_method,
                delivery_charge=delivery_charge,
                total=total,
                delivery_date=delivery_date,
                card_details=data.get("card_details", {}),
            )

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


# ✅ CREATE RAZORPAY ORDER (for online payments)
class RazorpayOrderCreateAPIView(APIView):
    def post(self, request):
        try:
            amount = request.data.get("amount")

            if not amount:
                return Response(
                    {"error": "Amount required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            data = {
                "amount": int(float(amount) * 100),  # amount in paise
                "currency": "INR",
                "payment_capture": 1,
            }

            payment = client.order.create(data=data)
            return Response(payment, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


# ✅ VERIFY RAZORPAY PAYMENT SIGNATURE
class RazorpayVerifyAPIView(APIView):
    def post(self, request):
        try:
            razorpay_order_id = request.data.get("razorpay_order_id")
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_signature = request.data.get("razorpay_signature")

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return Response(
                    {"error": "Missing payment details"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 🔒 Verify signature
            generated_signature = hmac.new(
                bytes(settings.RAZORPAY_KEY_SECRET, "utf-8"),
                msg=bytes(razorpay_order_id + "|" + razorpay_payment_id, "utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest()

            if generated_signature == razorpay_signature:
                return Response(
                    {"message": "✅ Payment verified successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "❌ Verification failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


# ✅ GENERIC ORDER VIEW (Fetch or Create if needed)
class OrderAPIView(APIView):
    def get(self, request):
        """Fetch all orders for logged-in user"""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        orders = Order.objects.filter(user=request.user).order_by("-purchased_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Fallback create route if needed"""
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
