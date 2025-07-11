export const getAnimals = async () => {
  try {
    const response = await fetch(`/api/animals`, { method: "GET" });
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
    console.log(`Making request to: /api/animals`);
    const response = await authFetch(`/api/animals`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(animal),
    });
    if (!response.ok) {
      throw new Error("Error creating animal profile");
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

export const uploadAnimalImages = async (authFetch, animalId, formData) => {
  try {
    console.log(`Making request to: /api/animals/${animalId}/upload-images`);
    const response = await authFetch(`/api/animals/${animalId}/upload-images`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error("Error uploading images");
    }
    const data = await response.json();
    console.log('image data:', data)
    return {
      status: response.status,
      message: "Received image data",
      data: data,
    };
  } catch (error) {
    console.error("Fetch error:", error);
    throw error;
  }
};

export const getSingleAnimal = async (id) => {
  try {
    const response = await fetch(`/api/animals/${id}`, { method: "GET" });
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
export const editAnimal = async (authFetch, animalId, updatedAnimalData) => {
  const requestOptions = {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updatedAnimalData),
  };

  try {
    console.log(`Making request to: /api/animals/${animalId}`);
    const response = await authFetch(
      `/api/animals/${animalId}`,
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

export const updateAnimalActiveStatus = async (
  authFetch,
  animalId,
  isActive
) => {
  const requestOptions = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    const response = await authFetch(
      `/api/animals/${animalId}/change_isactive`,
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
