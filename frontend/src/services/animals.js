

export const getAnimals = async () => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
    },
  };
  try {
    const response = await fetch(`/api/listings`, requestOptions);
    if (response.status !== 200) {
      throw new Error("Unable to fetch animals");
    }
    const data = await response.json();
    return data || [];
  } catch (error) {
    console.error("Error:", error);
    return [];
  }
};

export const createAnimal = async (authFetch, animal) => {
  try {
    console.log(`Making request to: /api/listings`);
    const response = await authFetch(`/api/listings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(animal),
    });
    if (!response.ok) {
      throw new Error("Error creating post");
    }
    const data = await response.json();
    return {
      status: response.status,
      message: "Successfully created animal profile",
      data: data,
    };
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getSingleAnimal = async (id) => {
  const requestOptions = {
    method: "GET",
    headers: {
      // Authorization: `Bearer ${token}`,
    },
  };
  try {
    const response = await fetch(
      `/api/listings/${id}`,
      requestOptions
    );
    if (response.status !== 200) {
      throw new Error("Unable to fetch this animal");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
  }
};

// export const getProfileImage = async (id) => {
//   const requestOptions = {
//     method: "GET",
//   };
//   try {
//     const response = await fetch(
//       `/api/assets/images/${id}`,
//       requestOptions
//     );
//     if (!response.ok) {
//       const errorText = await response.text();

//       if (response.status == 404) {
//         throw new Error(errorText);
//       } else {
//         throw new Error("Unable to fetch profile image");
//       }
//     }

//     const imageBlob = await response.blob();

//     const imageUrl = URL.createObjectURL(imageBlob);
//     return imageUrl;
//   } catch (error) {
//     console.error("Error:", error);
//   }
// };

// /**
//  * This function allows a user to edit an existing animal listing
//  * @param token (authentication),
//  * @param animalID of animal to be edited,
//  * @param updatedAnimalData - new data to be written in database
//  * Makes a request to backend URL for PUT request
//  * Returns success message, response status, and added data
//  */
export const editAnimal = async (token, animalId, updatedAnimalData) => {
  const requestOptions = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(updatedAnimalData),
  };

  try {
    console.log(`Making request to: /api/listings/${animalId}`);
    const response = await fetch(
      `/api/listings/${animalId}`,
      requestOptions
    );

    if (!response.ok) {
      throw new Error("Error updating animal profile");
    }

    const data = await response.json();
    return {
      status: response.status,
      message: "Successfully updated animal profile",
      data: data,
    };
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

// This function changes the isActive state to be set to False
// Makes a PUT request to change isActive field in db to 'false'

export const updateAnimalActiveStatus = async (token, animalId, isActive) => {
  const requestOptions = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ isActive }),
  };

  try {
    const response = await fetch(
      `/api/listings/${animalId}/change_isactive`,
      requestOptions
    );

    if (!response.ok) {
      throw new Error("Error updating animal status");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};
