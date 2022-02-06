# Django-Rest-Framework

`API`
- intermediary(waiter)
    * private
    * partner
    * public
    
`Web API`
    web applications api --- web api
    need api key/token . request to the server get data
    
`REST`
    -> guideline for making API
   
`RESTFUL API/ REST API`
    using rest 
    
www.testapi.com/api/users 
www.testapi -> base url
/api/ -> naming convention
/users/ -> api/Endpoint

`Django Rest Framework`
    - pip install djangorestframework
    
`Serializers`
    * python JSON -> package(builtin) -> use for JSON data
    * dumps (data) convert python object into JSON string 
        - Import Json
    * loads(data) -> parse json string(JSON format -> string(python) convert
    
    p->j = dumps(data)
    j->p = loads(data)
    
    * serializers are responsible for converting complex data such as querysets and model instances to native python datatypes than 
    it can be easily rendered into json,xml to frontend
    
    * serializer class like as django form 
        - create serializers.py
        - Import (from rest-framework import serializers)
        - class serializerName(serializers.Serializer)
        
    * p->j/j->p called serialization
        - create a instance first then pass that into the serializer
        - stu = Student.objects.get(id=1)
        - serializer = StudentSerializer(stu)
        - serializer.data
       
`JSONRENDER`
    stu = Student.objects.get(id=1)
    serializer = StudentSerializer(stu)
    json_data = JSON().render(serializer.data)
    
# we can write create/update/get function inside the serializers

`Filed Validation`
    - validate specific filed
        -validate_roll(self, value):
            if.........
            
            
`Model Serializer Class`
    - no need to write model fields
    - all are same as Serializer class
    - create/update functions are implemented by default
    Class Meta: (indicate Model class)
        model = model name
        fields = ["", ""]/ __all__
        exclude=[" "]
        read_only_fields  = [" "]
        extra_kwargs = {"field": {"read_only": True}}
        
        
`Function Based API`
    -@api_view() (decorators)
    -@api_view(['GET', ....]) 
    -from rest-framework.decorators import api_view
    
    * request.data-> return the parsed content of the request body. This is similiar to the standard request.POST and request.FILES
    * request.query.params-> same as request.GET/ good to use request.query.params
    * headers = application/json
    
`Class Based API View`
    -from rest-framework.decorators import APIView
    - Class StudentAPI(APIView):
        def ........ all are same as function based view
        

`Generic View`
    - This class extends REST Frameworks APIView class, adding commonly required behavior for standard list and detail views.
    #Attributes
        - queryset 
        - serializer_class
        - lookup_field
        - lookup_url_kwarg
        - pagination_class
        - filter_backends
    #Methods
        - get_queryset(self)
        - get_object(self)
        - get_serializer_class(self)
        - get_serializer_context(self)
        - get_serializer(self, instance=None, data=None, many=False, partial=False)
        - get_paginated_response(self, data)
        - paginate_queryset(self, queryset)
        - filter_queryset(self, queryset)
    #Mixins
        - ListModelMixin(list method, listing queryset)
        - CreateModelMixin(create method, creating and saving a new model instance)
        - RetrieveModelMixin(retrieve method, existing model instance)
        - UpdateModelMixin(update method, updating and saving an existing model instance)
        - DestroyModelMixin(destroy method, deletion)

`Concrete View Class`
    * Extends: Generic and Mixins inherits
    - ListAPIView
    - CreateAPIView
    - RetrieveAPIView
    - UpdateAPIView
    - DestroyAPIView
    - ListCreateAPIView
    - RetrieveUpdateAPIView
    - RetrieveDestroyAPIView
    - RetrieveUpdateDestroyAPIView
    
`ViewSet Class`
   - combine relative views in a single class
   - provide actions(create, update, delete, list, retrieve, partial_update) instead of methods(post, get)
  
  
`ModelViewSet Class`
   - inherits from GenericAPIView includes implementations for various actions, by mixing in the behavoiur of the various mixin class. 
   
`Authentication & Permission`
   - permissions(AllowAny, isAuthenticate, isAdminUser, )
