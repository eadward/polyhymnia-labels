import streamlit as st
import pandas as pd
import numpy as np
import random, os, csv, time #, datetime

def count_annotated_tuples(filename,min_index, max_index):
  """Counts the occurrences of each item in the fifth column of a CSV file.

  Args:
    filename: The name of the CSV file.

  Returns:
    A dictionary where keys are column 5 values and values are their counts.
  """

  item_counts = {}
  with open(filename, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip header

    for row in csv_reader:
      item_counts[row[0]] = item_counts.get(row[0], 0) + 1

  print(item_counts)
  index = np.arange(min_index, max_index) # + 1)
  df = pd.DataFrame({'count': [item_counts.get(str(i), 0) for i in index]}, index=index)
  df.index.name = 'tuple_idx'
  return df

def append_to_csv(filename, data):
  """Appends a line with the given data to a CSV file.

  Args:
    filename: The name of the CSV file.
    data: A list of six values to be appended as a row.
  """

  write_header = 1 if not os.path.exists(filename) else 0
    
  with open(filename, 'a', newline='') as csvfile:
            
    csv_writer = csv.writer(csvfile)
    # Check if the file is empty to write the header
    if write_header:
      csv_writer.writerow(['tuple_idx','hA','lA','hV','lV','timestamp'])
    timestamp = int(time.time()) # datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow(data+[timestamp])  
    # csv_writer.writerow(data)

def process_data(t,ha,la,hv,lv):
    append_to_csv(annot_file, [tuple,hA,lA,hV,lV])
    print("save data!")
    st.write("Tuple IDX: ", tuple) 
    st.write("Highest Arousal: ", hA) 
    st.write("Lowest Arousal: ", lA)
    st.write("Highest Valence: ", hV)
    st.write("Lowest Valence: ", lV)
    return annot_file

def select_pseudorandom_tuple(df):
    """Selects a random item from the DataFrame, prioritizing items with lower counts.

    Args:
        df: The input DataFrame.

    Returns:
        The selected item (index) from the DataFrame.
    """

    # Create a weighted probability based on inverse count
    #weights = 1 / df['count']
    weights = df['count'].apply(lambda x: 1e-9 if x == 0 else 1 / x)
    weights /= weights.sum()  # Normalize weights
    # Select a random item based on weights
    selected_index = df.sample(weights=weights).index[0]
    return selected_index


st.set_page_config(layout="wide")
st.title("Polyhymnia :orange[Labels]")
annot_file = os.path.join('data','annotations.csv')
# items = pd.read_csv("./data/items.csv")
tuples = pd.read_csv("./data/tuples.csv")
tuples_annot_counter = count_annotated_tuples('./data/annotations.csv',0,tuples.shape[0])
tuples_annot_counter = tuples_annot_counter[tuples_annot_counter['count'] <= 2]

if not tuples_annot_counter.empty:

    tuple = select_pseudorandom_tuple(tuples_annot_counter)
    #tuple = random.randrange(0,tuples.shape[0])
    st.markdown("Tuple :blue[" + str(tuple) + "] (" + str(tuples_annot_counter.loc[tuple,'count']) + " annotations)")
    num_tuples = len(tuples.columns) 
    song_cols = st.columns(np.ones((num_tuples,), dtype=int))
    for i,col in enumerate(tuples.columns):
        with song_cols[i]:
            st.subheader(tuples.columns[i])
            st.audio("./data/tracks/"+str(tuples[tuples.columns[i]][tuple])+".mp3", format="audio/wav")
    # col1, col2, col3, col4 = st.columns([1,1,1,1])
    # with col1:
    #     st.subheader(tuples.columns[0])
    #     st.audio("./data/tracks/"+str(tuples[tuples.columns[0]][tuple])+".mp3", format="audio/wav")
    # with col2:
    #     st.subheader(tuples.columns[1])
    #     st.audio("./data/tracks/"+str(tuples[tuples.columns[1]][tuple])+".mp3", format="audio/wav")
    # with col3:
    #     st.subheader(tuples.columns[2])
    #     st.audio("./data/tracks/"+str(tuples[tuples.columns[2]][tuple])+".mp3", format="audio/wav")
    # with col4:
    #     st.subheader(tuples.columns[3])
    #     st.audio("./data/tracks/"+str(tuples[tuples.columns[3]][tuple])+".mp3", format="audio/wav")


    with st.form("my_form"):

        st.subheader("Please listen to the four songs above and indicate which track has the …")

        hA = st.radio(
            "... **HIGHEST** :red[Arousal].",
            tuples.columns, horizontal=True, index=None)

        lA = st.radio(
            "... **lowest** :red[Arousal].",
            tuples.columns, horizontal=True, index=None)

        hV = st.radio(
            "... **HIGHEST** :green[Valence].",
            tuples.columns, horizontal=True, index=None)

        lV = st.radio(
            "... **lowest** :green[Valence].",
            tuples.columns, horizontal=True, index=None)

        submitted = st.form_submit_button("Submit") #, on_click=process_data, args=[tuple,hA,lA,hV,lV])
        if submitted:
            if hA == None or lA == None or hV == None or hV == None:
                st.error("Please make sure that you answer all questions.")  
            else:
                process_data(tuple,tuples[hA],tuples[lA],tuples[hV],tuples[lV])
                
            # save to file: how to save data?

    with st.expander("Help ..."):
        st.write('''
            .....
        ''')
        st.image("https://static.streamlit.io/examples/dice.jpg")

else:
    st.markdown("No annotation tasks available.")
