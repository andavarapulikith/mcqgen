from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

load_dotenv()

key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(openai_api_key=key,model="gpt-3.5-turbo",temparature=0.5)


