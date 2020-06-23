import streamlit as st
import pickle
import altair as alt

@st.cache
def read_data():
    with open('disinfo_data.pickle', 'rb') as h:
        return pickle.load(h)

@st.cache
def unique_fos_level(df):
    return sorted(df['level'].unique())

def unique_fos(df, level, num):
    return list(df[df['level']==level].name.value_counts().index[:num])

def main():
    data = read_data()
    fos_level = unique_fos_level(data)

    st.title("Misinformation research explorer")

    filter_year = st.sidebar.slider("Filter by year", 2000, 2020, (2000, 2020), 1)
    filter_fos_level = st.sidebar.selectbox(
        "Choose Field of Study level", fos_level)
    fields_of_study = unique_fos(data, filter_fos_level, 15)
    filter_fos = st.sidebar.multiselect(
        "Choose Fields of Study", fields_of_study)

    if filter_fos:
        frame = data[(data.name.isin(filter_fos)) & (data.year>=str(filter_year[0])) & (data.year<=str(filter_year[1]))].drop_duplicates('id')
        color_on_fos = True
    else:
        frame = data[(data.year>=str(filter_year[0])) & (data.year<=str(filter_year[1]))].drop_duplicates('id')
        color_on_fos = False

    if color_on_fos:
        chart = alt.Chart(frame).mark_point().encode(
            alt.X('Component 1', scale=alt.Scale(domain=(3, 14))),
            alt.Y('Component 2', scale=alt.Scale(domain=(7, 16))),
            alt.Color('name'),
            alt.Size('citations', scale=alt.Scale(range=[10,500]), title='Citations'),
            href='source:N',
            tooltip=['title', 'year']
        ).interactive().properties(width=650, height=500)

    else:
        chart = alt.Chart(frame).mark_point().encode(
            alt.X('Component 1', scale=alt.Scale(domain=(3, 14))),
            alt.Y('Component 2', scale=alt.Scale(domain=(7, 16))),
            alt.Size('citations', scale=alt.Scale(range=[10,500]), title='Citations'),
            href='source:N',
            tooltip=['title', 'year']
        ).interactive().properties(width=650, height=500)

    st.altair_chart(chart, use_container_width=True)

    st.subheader("How to use this app")
    st.write(f"""
    This applications is intended for visual exploration and discovery of research publications on misinformation, disinformation and fake news. Every particle in the visualisation is an academic publication. The particles are positioned in space based on the semantic similarity of the paper abstracts; the closer two points are, the more semantically similar their abstracts. You can hover over the particles to read their titles and you can click them to be redirected to the original source. You can zoom in the visualisation by scrolling and you can reset the view by double clicking the white space within the figure. 

#### Filters
You can specify a range for the papers' publication date. You can also show papers with a particular set of fields of study. Microsoft Academic Graph uses a 6-level hierarchy where level 0 is high level disciplines such as Biology and Computer science while level 5 contains the most granular paper keywords. Using the sidebar filters, you can first choose the level of the field of study and then pick specific keywords within it. 
    """)

    st.subheader("About")
    st.write(
            f"""
This prototype is part of [Orion](https://orion-search.org/), a knowledge discovery and research measurement tool I am developing for my Mozilla Fellowship in collaboration with Zac Ioannidis and Lilia Villafuerte.

If you have any questions or would like to learn more about it, you can find me on [twitter](https://twitter.com/kstathou) or send me an email at kostas@mozillafoundation.org
    """
        )

    st.subheader("Appendix: Data & methods")
    st.write(f"""
    I collected all of the publications from [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/academic-knowledge/) that were published between 2000 and 2020 and contained one of the following terms as a field of study:
- misinformation  
- disinformation  
- fake news  

I fetched approximately 15K publications. This visualisations shows only those with a DOI - that's ~5K documents.

To create the 2D visualisation, I encoded the paper abstracts to dense vectors using a [sentence-DistilBERT](https://github.com/UKPLab/sentence-transformers) model. That produced a 768-dimensional vector for each document which I projected to a 2D space with [UMAP](https://umap-learn.readthedocs.io/en/latest/). 
""")

if __name__ == '__main__':
    main()
