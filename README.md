# Ebay Alert system

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Endpoints](#Endpoints)
* [Resources](#Resources)

## General info:
 This project is an ebay product price alert notification system which allows users to create alert for their search
 phrases by passing search_phrase, time_intervals and email_id as inputs. User will get product alert in every 2,10,30
 time intervals based on their settings. User will also get notification if there is price decrease or if price doesn't
 change in specified time intervals.

## Scope of functionality:
 ### Phase 1:
  * Product alert can be managed from UI.
    * Product alert can be created and viewed from UI. User Authentication is not covered in this project.
    * Time interval is `2`, `10`, `30` in this project scope.
    * Only created and view alert is covered in UI and all CRUD application can be done from swagger interface which
      is available on `http://127.0.0.1:8000/api-doc`
    * Product alert is saved in `ProductAlert` table
    * Assumption:
       * Only one alert can be created for a particular search phrase and email id.

  * Product alert notification service.
    * This service run every 1 minute and fetched products for all created product alerts and save it in product table.
    * This service checks if update is already sent in user's set time intervals and send update by searching search
      phrase on ebay and saving that data in product and price table.
    * We have added table as `update` to store update sent related to alert and product table to store product searched
      for a particular search phrase.Price is stored in separate
      price table to store the log of price change for that particular product.
    * Assumptions:
       * Ebay itemId will be unique.
       * Sorted by: price. This value can be changed from env file.
       * Limit: 20. This value also can be changed from env file.
       * This service will run every 1 minutes to send notification for product alert data.

  ### Phase 2:
* This service check if there is price decrease or no change in price and send alert to user to take action
      on that particualr product.
    * This service will run every 2 days at 12 Noon.
    * Product alert will be sent if there is:
      * 1. No price change.
      * 2. Price decreased by 2 percent.
      * 3. Cheaper price is available.
    * This service will also publish these products info on queue which can be subscribed by `Team B`
      to perform action on these alerts and product insight.
    * Implementation for second project for `Team B` is a simple script implemented as a consumer which
      listen to the queue and printing messages.
    * Assumptions:
       * This service perform insight on product price for last 2 days which can be configured from env file.
       * Redis port is exposed as of now for `Team B` to listen which is not a secure way.
         Please make sure this port is free on your system.

## Technologies:
   ### Framework:
   * Django: Because web development is faster in Django.
   * Django rest framework: For crud api applications and integration with Swagger.
   * Django swagger: For Api documentations.
   * NextJs: Because it's fast and it avoid writing boilerplate code.

   ### Database:
   * Postgres : For relational database.
   ### Message broker and task scheduler:
   * Redis: For queue and message broker.
   * Celery: To schedule task in the background.
   ### Deployments:
   * Docker: For deployment and running the project

## Setup
* build the applicationq
    ``docker-compose build``

* Run the application
    ``docker-compose up``

* Rename .env.example to .env and replace the value in .env
# Endpoints:

* Server application: `http://127.0.0.1:8000`
  * Api doc (swagger): `http://127.0.0.1:8000/api-doc`
  * Client  application: `http://127.0.0.1:300`

please make sure these ports are free on your host system

### Resources:
* css: https://github.com/andybrewer/mvp/
* next docker image: https://nextjs.org/docs/deployment
* email html boilerplate: https://github.com/leemunroe/responsive-html-email-template
