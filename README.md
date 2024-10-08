# App preview

Homescreen - key image selection

![](report/img/key_selection.png)

Query result - most similar images, based on given parameters

![](report/img/similar_results.png)

# 🇬🇧 SIMages - Similarity join on image database

A web application for the similarity connection of one image, the so-called key, with a set of images. Images are compared based on the VGG-16 convolutional neural network embeddings (activations of the final dense layer). The application will load the available image sets from the appropriate directory and allow the user to interactively select the key and image set. At the same time, the user has several search parameters at his disposal, such as the selection of a predicate (kNN, range) and its parameter or the selection of a metric (cosine similarity, Euclidean distance). The user will then see his chosen key image on a new screen, together with connected images sorted from most similar according to the chosen metric.

After completing the query, the user has the option to continue editing it, either by changing the search parameters or selecting a new key image. For clarity, the application always displays only similarity connections for one key image. With this approach, the application tries to simulate the appearance of recommendation algorithms of various web services. It is therefore a simple recommendation algorithm based on content, which for practical use in an online service could be supplemented with, for example, a collaborative filtering algorithm, i.e. recommendations based on the activity of other users.

See [the full report 🇨🇿](report/report.pdf) for more details. The project was created as a semester project at FIT CTU in the course BI-VWM.

## How to run

Initialize a new conda environment from the included config file:
```
conda env create -f environment.yml
```

Load the images into one or more datasets:
```
mkdir -p data/set01 [data/set02 ...]
cp [your images] data/set01
...
```

Run the app:
```
python __main__.py
```

If the data directories were created correctly, the list of your datasets should be visible in the top-left. Changing the "Key Image Directory" changes the photo selection on the screen.

# 🇨🇿 SIMages - Podobnostní spojení na databázi obrázků

Webová aplikace pro podobnostní spojení jednoho obrázku, tzv. klíče, se sadou obrázků. Obrázky jsou porovnávány na základě deskriptorů vygenerovaných konvoluční neuronovou sítí VGG-16. Aplikace nahraje dostupné sady obrázků z příslušného adresáře a umožní uživateli interaktivní výběr klíče a sady obrázků. Zároveň má uživatel k dispozici několik parametrů vyhledávání, jako je výběr predikátu (kNN, rozsahový) a jeho parametru nebo výběr metriky (cosinová podobnost, Euklidovská vzdálenost). Uživateli se následně na nové obrazovce zobrazí jeho zvolený klíčový obrázek, společně se spojenými obrázky seřazenými od nejpodobnějších podle zvolené metriky.

Po dokončení dotazu má uživatel možnost jej nadále upravovat, buď změnou parametrů vyhledávání nebo výběrem nového klíčového obrázku. Pro přehlednost aplikace vždy zobrazuje pouze podobnostní spojení pro jeden klíčový obrázek. Aplikace se tímto přístupem snaží simu- lovat vzhled doporučovacích algoritmů různých webových služeb. Jedná se tedy o jednoduchý algoritmus doporučování na základě obsahu, který by pro praktické použití v on-line službě mohl být doplněn např. o algoritmus kolaborativního filtrování, tedy doporučení na základě aktivity jiných uživatelů.

Další podrobnosti jsou obsaženy v [závěrečném reportu 🇨🇿](report/report.pdf). Projekt vznikl jako semestrální práce na FIT ČVUT do předmětu BI-VWM.