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
            
            