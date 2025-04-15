//animals pages page  

import { useState, useEffect } from "react";
import { getAnimals } from "../../services/animals";
import AnimalCard from "../../components/AnimalCard/animalcard";

// This component fetches all the animals from the database and displays them in a card format.
const AllAnimals = () => {
  const [animalsState, setAnimalsState] = useState([]);

  const fetchAnimals = () => {
    getAnimals()
      .then((data) => {
        console.log("I have data");

        if (data && Array.isArray(data  )) {
          setAnimalsState(data);
        } else {
          console.error("Unexpected data format:", data);
        }
      })
      .catch((err) => {
        console.error("Error fetching animals:", err);
      });
  };

  useEffect(() => {
    fetchAnimals();
  }, []);

  return (
    <>
      <h2>Can you give one of us a good home?</h2>
      {animalsState.length > 0 ? (
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "20px", 
          }}
        >
          {animalsState.map((animal) => {
            const { id, image, name, breed, age, location, shelter_id } = animal;
            console.log ("Image from DB: " + image);
            return (
              <div
                key={id} 
                style={{
                  flex: "1 1 calc(33.333% - 20px)", 
                  maxWidth: "calc(33.333% - 20px)",
                }}
              >
                <AnimalCard
                  id={id}
                  image={image}
                  name={name}
                  age={age}
                  breed={breed}
                  location={location}
                  button1Text={`Meet ${name}`}
                  linkUrl={`/animals/${id}`} 
                  shelter_id={shelter_id}
                              />
              </div>
            );
          })}
        </div>
      ) : (
        <p>No animals available at the moment.</p>
      )}
    </>
  );
};

export default AllAnimals;