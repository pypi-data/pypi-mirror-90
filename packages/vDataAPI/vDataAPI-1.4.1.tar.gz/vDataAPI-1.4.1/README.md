# vData.PL - Python API Lib
<hr />

### Example - Generate client
```py
from vDataAPI.Payments import VDataPayments
vdataclient = VDataPayments('callbackURI', 'redirectURI', 'apikey')
```

### Example - Generate payment
**Return JSON**
```python
payment = vdataclient.generate_payment(amount=12.50)
```


### Example - Check payment status
```python
paymentstatus = vdataclient.check_payment_status("PAYMENT ID")
```


By &copy; HSCode.PL