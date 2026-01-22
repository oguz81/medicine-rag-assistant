EN/TR
# MEDICINE ASSISTANT
Medicine Assistant is a RAG application that answers your asks and requests about medicines. It retrieves all about medicines only from medicine leaflets, like reading the paper comes with the medicine box
and telling you.

This assistant will assist only for Turkish medicines which all are registered by Turkish Medicine and Medical Device Department [TİTCK](titck.gov.tr). All leaflets will be retrieved from the website of the department.

This project is still being developed. When it's ready, you can find the web address here to ask about medicines.

## Backend 
Backend has ChromaDB, FastAPI, Uvicorn and gpt-4o-mini from OpenAI as LLM model.
## Frontend
Frontend has Streamlıt in this project.

# İLAÇ ASİSTANI
Bir RAG uygulaması olan İlaç Asistanı, ilaçlar ile ilgili kullanıcının sorularına cevap vermek üzere geliştirilmiştir. İlaç yan etkileri, kullanım şekli, hangi rahatsızlıklarda kullanılabileceği gibi
bilgileri ilacın kendi prospektüsünden alarak kullanıcıya aktarır. İlaç Asistanı'nın başvurduğu tüm prospektüsler, [Türkiye İlaç ve Tıbbi Cihaz Kurumu](titck.gov.tr)'nun internet sayfasında bulunan
ilaçların üreticileri tarafından yazılan ve kutulara konan belgelerdir.

Uygulama halen geliştirme aşamasındadır. Kullanıma hazır olduğunda çevrimiçi olarak erişilebilecektir.

## Backend
ChromaDB, FastAPI, Uvicorn ve dil modeli olarak gpt-4o-mini (OpenAI) kullanılmıştır.

## Frontend
Streamlit kullanılmıştır.
