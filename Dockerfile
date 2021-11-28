FROM heinzdf/Bot:buster
 
# Clone repo and prepare working directory
RUN git clone -b sql-extended https://github.com/jefanya14/Bot /Bot
RUN chmod 777 /Bot
WORKDIR /Bot
 
# Copies session and config (if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /root/userbot/
 
# Install requirements
CMD ["python3","-m","userbot"]
