# pull base image 

FROM nginx:1.24.0

COPY nginx/nginx.conf /etc/nginx/nginx.conf 

RUN mkdir /etc/nginx/sites-enabled 

RUN rm -r /etc/nginx/conf.d/*.conf

COPY nginx/sites-available/ /etc/nginx/sites-available/ 

RUN ln -s /etc/nginx/sites-available/cheaper_phone /etc/nginx/sites-enabled/cheaper_phone 

WORKDIR /data

COPY web_dynamics/static static/
