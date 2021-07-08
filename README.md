# product_recommender
## The Data Sets
I used datasets from [amzon product review](https://nijianmo.github.io/amazon/index.html), I've choosed __Arts, Crafts and Sewing *(meta & core5 )*__ becuase the size is small
* This Dataset is an updated version of the Amazon review dataset released in 2014. As in the previous version,

* this dataset includes reviews (ratings, text, helpfulness votes), product metadata (descriptions, category information, price, brand, and image features),

* I used datasets from amazon product review. I've chosen Arts, Crafts and Sewing (rating only, meta & core5) because the size is relatively small.

* The datasets was zipped format and need to parse and clean.

 ## The Data Sets in details
 1. rating only dataset :9447882 records, 4 columns
 * important columns:<br>
  ![image](https://user-images.githubusercontent.com/43261845/125000429-abd80a80-e050-11eb-96eb-ade1b9004153.png)
 2. Meta: 302988 records, 18 columns.
 * important columns: <br>
 ![image](https://user-images.githubusercontent.com/43261845/125000579-fce7fe80-e050-11eb-8cf1-6154341fb7c1.png)
3. core_5 data set: 494485 record, 12 columns.
. important columns: <br>
![image](https://user-images.githubusercontent.com/43261845/125000626-19843680-e051-11eb-95aa-db4f9be4c611.png)

the data sets after parsing and extractedfrom zipped format [here!](https://drive.google.com/drive/folders/1YXt1mw1pKU6XpZCtg7S5CjsNlipne7wc?usp=sharing)<br>


## cleaning data <br>
1. delete products with more than one product_id(asin)
```sql
with meta_titles(title,counts)
as
(
SELECT title,count(DISTINCT asin) counts from meta  
GROUP by title
HAVING counts > 1
)

DELETE from meta where meta.title in (SELECT title from meta_titles)
```
2. delete users with morethan one id
```sql
with core_names (reviewerName,counts)
as
(
SELECT reviewerName,count(DISTINCT reviewerID) counts from core5
GROUP by reviewerName
HAVING counts != 1
)
DELETE from core5 where reviewerName in (SELECT reviewerName from core_names)

```
3. delete users with more than on name
```sql
with core_ids(reviewerID,counts)
as
(
SELECT reviewerID ,count(DISTINCT reviewerName) counts from core5
GROUP by reviewerID
HAVING counts != 1
)
DELETE from core5 WHERE reviewerID in (SELECT reviewerID from core_ids)
```
4. create new table **(final dataset)** from joining two tables after cleaning
```sql
CREATE TABLE arts_crafts
as
SELECT ratings.asin,meta.title, core5.overall as rating,
meta.brand, meta.main_cat,meta.price,
meta.image, core5.reviewer ID as userId, core5.reviewer Name as username
from ratings
join meta on meta.asin = ratings.asin
join core5 on core5.asin = ratings.asin and core5.reviewerID = ratings.userid
```
## Final Dataset
* 53956 record, 9 column
* 15589 products <br>
![image](https://user-images.githubusercontent.com/43261845/125000838-8ef00700-e051-11eb-9ea7-3cadfad97e91.png)

## integrated dataset used in the model: 
1. [arts_craftss](https://drive.google.com/drive/folders/1YXt1mw1pKU6XpZCtg7S5CjsNlipne7wc?usp=sharing)<br>
2. result after building th model [arts_crafts_result](https://drive.google.com/file/d/1s_QA4002tgUaOj89HwXgdcusEsSX6AfQ/view?usp=sharing)<br>

this plot shows how the density of the dataset , as we see most products have only few rating this means sparse issue and so that I used SVD algo<br>

![image](https://user-images.githubusercontent.com/43261845/118348903-957c6980-b54d-11eb-82c9-a24e1cc93eda.png)

**snapshot of the API**<br>
![image](https://user-images.githubusercontent.com/43261845/118349238-d4132380-b54f-11eb-8fc6-de31a60ee68c.png)

