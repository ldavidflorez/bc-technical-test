## File Integrity Checker

Este proyecto consiste en una infraestructura montada en AWS diseñada para verificar la integridad de archivos. El usuario carga un archivo de texto plano en un bucket de S3 que contiene, entre otras cosas, un HASH calculado con MD5. Cuando el archivo se sube, es procesado por una función Lambda de AWS, que extrae la información del archivo y calcula su HASH MD5. La información contenida en el archivo se almacena en una tabla de DynamoDB, junto con otros detalles relevantes que proporcionan información sobre la integridad del archivo.

Para ejecutar el proyecto de forma local, puedes clonar este repositorio, dirigirte a la carpeta principal y ejecutar el siguiente comando para instalar las dependencias:

```bash
pip install -r requirements.txt
```

Se recomienda realizar esto dentro de un entorno virtual de Python. Una vez instaladas las dependencias, procede a ejecutar los siguientes comandos:

```bash
cd local/
python main.py
```

Si deseas ejecutar los tests unitarios de la aplicación localmente, puedes ejecutar:

```bash
pytest
```

Además, se proporciona un informe de cobertura de los tests en local/tests/htmlcov.

Finalmente, la carpeta lambda-aws contiene un archivo llamado lambda_function.py, que encapsula toda la funcionalidad necesaria para ejecutar la aplicación en AWS Lambda Function. Recuerda que debes configurar los permisos de la Lambda Function previamente para asegurar el correcto funcionamiento, esto incluye otorgar acceso al bucket de S3 y a la tabla de DynamoDB. También es importante añadir un disparador manualmente a tu Lambda Function para que sea activada cuando llegue un nuevo archivo al bucket de S3.

NOTA: El último paso mencionado no pudo ser verificado debido a que el recurso Lambda asignado no tiene los privilegios suficientes:

```bash
Calling the invoke API action failed with this message: User: arn:aws:iam::223690032992:user/luis-david is not authorized to perform: lambda:InvokeFunction on resource: arn:aws:lambda:us-east-1:223690032992:function:ai-technical-test-luis-david because no identity-based policy allows the lambda:InvokeFunction action
```