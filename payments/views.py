
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from payments.models import Invoice
from payments.serializers import InvoiceSerializer

# Vista para crear facturas (solo administradores pueden hacerlo)
@api_view(['POST'])
@permission_classes([IsAdminUser])  
def create_invoice(request):
    
    amount = request.data.get('amount')
    status_value = request.data.get('status', 'pending')  # Si no se proporciona, por defecto será 'pending'

    if not amount:
        return Response({"error": "El campo 'amount' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

    # Crear la factura
    invoice = Invoice.objects.create(user=request.user, amount=amount, status=status_value)

    # Serializar la factura creada
    serializer = InvoiceSerializer(invoice)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Vista para obtener las facturas de un usuario autenticado
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Solo los usuarios autenticados pueden ver sus facturas
def get_user_invoices(request):
    
    user = request.user
    invoices = Invoice.objects.filter(user=user)

    # Serializar las facturas
    serializer = InvoiceSerializer(invoices, many=True)

    return Response(serializer.data)

# Vista para que el usuario marque la factura como pagada
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Solo los usuarios autenticados pueden pagar sus facturas
def pay_invoice(request, invoice_id):
   
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        return Response({"error": "Factura no encontrada o no pertenece a este usuario."}, status=status.HTTP_404_NOT_FOUND)

    # Cambiar el estado de la factura a "pagada"
    invoice.status = 'paid'
    invoice.save()

    # Serializar y devolver la factura actualizada
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data, status=status.HTTP_200_OK)
