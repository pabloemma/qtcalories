record =['a','bb','cc','dd','gg']
row_name ='shit'
b= row_name+','+record[0]+','+record[1]+','+record[2]+','+record[3]+','+record[4]
a = 'INSERT INTO recipes (name,energy,protein,carbohydrate,fat,ingredients) VALUES ('+b+');'
print(a)


#INSERT INTO "recipes" ("name","energy","protein","carbohydrate","fat","ingredients") VALUES ('roesti','1.87','0.10','0.13','0.11','110 g onion 107 g bacon 531 g potato 140 g raclette');
