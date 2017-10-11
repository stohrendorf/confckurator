import os
import shutil

os.chdir(os.path.dirname(__file__))

print("Removing old client API files...")
shutil.rmtree('../frontend/src/api')

print("Generating client API files from swagger API description...")
os.system(
    'java -jar swagger-codegen-cli-2.2.1.jar generate -i api.yml -l typescript-angular -o ../frontend/src/api')

print("Copying swagger API description to frontend...")
shutil.copy('api.yml', '../server/static/swagger/api.yml')

print("Client API generated.")
