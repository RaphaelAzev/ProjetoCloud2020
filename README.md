# ProjetoCloud2020
Projeto para computacao em nuvem

E necessário instalar as seguintes dependências:  
pip3 install boto3  
pip3 install awscli  
pip3 install requests  

Para configurar as credenciais da AWS rodar:  
aws configure

Para levantar o ambiente rodar:  
sh SetupAmbiente.sh (Essa etapa é demorada)  
(Rodar o SetupAmbiente com o ambiente ainda de pé irá destruí-lo e levantá-lo denovo)
  
Para destruir o ambiente:  
python3 ./PythonBotoFiles/DeleteAll.py  

Para usar o Client simples:  
python3 Client.py getAll --> Pega todas as tasks no banco de dados  
python3 Client.py postTask --> Adiciona uma tasks ao banco de dados  
  
Obs: Banco de dados começa vazio
