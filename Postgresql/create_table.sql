------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: Tweet
------------------------------------------------------------
CREATE TABLE public.Tweet(
	id                     SERIAL NOT NULL ,
	text                   VARCHAR (280) NOT NULL ,
	user_id                INT  NOT NULL ,
	user_name              VARCHAR (100) NOT NULL ,
	location               VARCHAR (100) NOT NULL ,
	user_friends_count     INT  NOT NULL ,
	user_followers_count   INT  NOT NULL ,
	timestamp              DATE  NOT NULL ,
	is_tweet_reply         BOOL  NOT NULL ,
	score                  FLOAT  NOT NULL ,
	topic                  VARCHAR (50) NOT NULL ,
	telecom_compagny       VARCHAR (50) NOT NULL  ,
	CONSTRAINT Tweet_PK PRIMARY KEY (id)
)WITHOUT OIDS;



