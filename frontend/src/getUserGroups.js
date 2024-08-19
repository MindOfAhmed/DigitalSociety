import axios from "axios";

// this function will return the user groups the logged in user is in
export const getUserGroups = async () => {
  // make a get request to the user groups endpoint
  try {
    const response = await axios.get("http://127.0.0.1:8080/api/user_groups/", {
      // pass the token in the headers
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });
    // check if response and response.data are defined
    if (response && response.data && response.data.groups) {
      return response.data.groups;
    } else {
      console.error("Invalid response structure", response);
      return [];
    }
    // copilot ^_^
  } catch (error) {
    console.error("Error fetching user gorups", error);
    return [];
  }
};
