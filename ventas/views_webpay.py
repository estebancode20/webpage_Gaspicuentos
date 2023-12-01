from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from .models import Compra, DetalleCompra, Libro

def pagar(request):
    return render(request, "carrito.html")

def pagar_send(request):
    print(request.GET['valor'])
    url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
    myobj = {
        "buy_order": "ordenCompra12345678",
        "session_id": "sesion1234564",
        "amount": request.GET["valor"],
        "return_url": "http://127.0.0.1:8000/ventas/boleta"
    }
    headers = {
        'Content-Type': 'application/json',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Tbk-Api-Key-Id': '597055555532'
    }

    resp = requests.post(url, json=myobj, headers=headers)
    print("header WepPay: ", resp.headers)
    print("\n\n text WebPay: ", resp.text)
    respuesta = json.loads(resp.text)
    print("token WebPay", respuesta["token"])
    print("url   WebPay", respuesta["url"])
    return redirect(respuesta["url"] + "?token_ws=" + respuesta["token"])
    # return render(request,"pagar_send.html")

def pagar_boleta(request):
    print("body", request.body)
    stToken = request.GET.get('token_ws')

    url = 'https://webpay3gint.transbank.cl//rswebpaytransaction/api/webpay/v1.2/transactions/' + stToken
    headers = {
        'Content-Type': 'application/json',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Tbk-Api-Key-Id': '597055555532'
    }

    respuesta = requests.put(url, headers=headers)
    print("\n\n header", respuesta.headers)
    print("\n\n text", respuesta.text)
    resWP = json.loads(respuesta.text)
    print("Vci         :", resWP["vci"])
    print("Monto         :", resWP["amount"])
    print("status         :", resWP["status"])
    print("Orden         :", resWP["buy_order"])
    print("sessionID         :", resWP["session_id"])
    print("Tarjeta         :", resWP["card_detail"])  # :{"card_number":"2222"}
    print("Feha         :", resWP["accounting_date"])
    print("Fecha Tran         :", resWP["transaction_date"])
    print("Autrizacion         :", resWP["authorization_code"])
    print("Código de Pago         :", resWP["payment_type_code"])
    print("response_Code         :", resWP["response_code"])
    print("installments         :", resWP["installments_number"])

    # Guardar los datos de la compra en las tablas Compra y DetalleCompra
    compra = Compra.objects.create(usuario=request.user)
    detalles_compra = []
    for item in request.user.carrito_set.all():
        detalle = DetalleCompra.objects.create(
            compra=compra,
            libro=item.libro,
            cantidad=item.cantidad,
            precio_unitario=item.libro.precio_venta,
            precio_total=item.precio_total
        )
        detalles_compra.append(detalle)

    # Limpiar el carrito del usuario después de completar la compra
    request.user.carrito_set.all().delete()

    # Incluir información de la compra y sus detalles en el diccionario de contexto
    context = {"vci": resWP["vci"], "data": resWP, "detalles_compra": detalles_compra}

    return render(request, "boleta.html", context)
