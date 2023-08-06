# Django Rest Error Inherits Error Messages
ModelSerializer inherits the error_messages of the model


## Example 
```
pip install django-rest-inherits-error-messages
```

Set error_messages in your model field.
models.py
```
class TestModel(django.db.models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, error_messages={'required':'[test] This field is required.'})
```

Go to your ModelSerializer and inherit the InheritsModelSerializer (InheritsHyperlinkedModelSerializer also exists)
```
class TestSerializer(InheritsModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'
```

If set as above, error_messages will be inherited.

## Contributions
Issues and PR are welcome.