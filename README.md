# Misinformation research explorer #

This application is intended for visual exploration and discovery of research publications on misinformation, disinformation and fake news. Every particle in the visualisation is an academic publication. The particles are positioned in space based on the semantic similarity of the paper abstracts; the closer two points are, the more semantically similar their abstracts. You can hover over the particles to read their titles and you can click them to be redirected to the original source. You can zoom in the visualisation by scrolling and you can reset the view by double clicking the white space within the figure.

## Filters ##

You can specify a range for the papers' publication date. You can also show papers with a particular set of fields of study. Microsoft Academic Graph uses a 6-level hierarchy where level 0 is high level disciplines such as Biology and Computer science while level 5 contains the most granular paper keywords. Using the sidebar filters, you can first choose the level of the field of study and then pick specific keywords within it.

## About ##

This prototype is part of Orion, a knowledge discovery and research measurement tool I am developing for my Mozilla Fellowship.

If you have any questions or would like to learn more about it, you can find me on [twitter](https://twitter.com/kstathou).

## Data and methods ##
I collected all of the publications from Microsoft Academic Graph that were published between 2000 and 2020 and contained one of the following terms as a field of study:

misinformation
disinformation
fake news
I fetched approximately 15K publications. This visualisations shows only those with a DOI - that's ~5K documents.

To create the 2D visualisation, I encoded the paper abstracts to dense vectors using a sentence-DistilBERT model. That produced a 768-dimensional vector for each document which I projected to a 2D space with UMAP.

## How to deploy the app locally with Docker ##
Assuming docker is running on your machine and you have a docker account, do the following:
- Build the image

``` bash
docker build -t <USERNAME>/<YOUR_IMAGE_NAME> .
```

- Run the image

``` bash
docker run -p 8501:8501 <USERNAME>/<YOUR_IMAGE_NAME>
```

- Open your browser and go to `http://localhost:8501/`
