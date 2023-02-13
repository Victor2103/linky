# Monitor your bills with your linky !

In this repository, we will learn how to create an interface to see our electric consumption. The tools used here are :
- Python3
- PostgreSQL with the extension timescaleDB 
- Grafana
- Telegram 
- Metabase

With grafana, at the end, you will see something like this :

![image](images/grafana.png)

And with Metabase it will be like this : 

![image](images/metabase.png)

Ok now, let's see how we create this result ! 

## Requirements



### Access to the Enedis APP

First of all, you need to get create an account on Enedis. To monitor your data, you need to acess the Enedis API. So to this, you have to create an account on Enedis and then access to get an application called `MyElectricalData`. 

After create your account on Enedis APP, get the number of your linky (this number is called the PDL number). You have to click on the button present on the electric meter. And you can check, there are lots on information on this meter ! Here is what it will look like : 

![image](images/pdl.png)

Now, add this number on the Enedis App. This will permits to have a first visualisation of your electric consumption of you want. But if we create an account, it is to tell Enedis that we allow `MyElectricalData` to get our electric data. Inside the Enedis APP, go to `Manage access to my data`. Then, you will be able to access the API `my electrical data`. The purpose to use this application is to access the Enedis API. Now, go on [MyElectricalData](https://www.myelectricaldata.fr/) and click on `faire la demande de consentement`. You will be redirect to the Enedis app and accept to transfer your data to `MyElectricalData`. This API is totally free but if you want to make a donation you can directly on the website. 

We have now access to the API. Don't forget to save your PDL and your token. You will need them after. We can collect our eletric consumption every 30 minutes. Let's do this ! 

### Get our electrical data 

To have our electrical data, it is very simple ! The commande to execute is in the repo git in the file `commande.env`. Just replace the token and the PDL with your values. If you want to simply copy and paste the command, go directly [here](https://www.myelectricaldata.fr/documentation), fill your token, your PDL, the start and end date where you want your electric consumption and copy the command located juste after `Récupérer la puissance moyenne consommée quotidiennement, sur l'intervalle de mesure du compteur (par défaut 30 min)`. 

And that's it. You have a json file with your electric consumption. But, how to display it ? And how to store it ? We will handle this in the next part of the tutorial with a PostGreSQL database, Grafana and Metabase. 

## Store your data with PostGreSql 

