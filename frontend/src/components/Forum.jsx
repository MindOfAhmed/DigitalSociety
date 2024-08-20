import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export const Forum = () => {
  // get the form id from the URL
  const { forumId } = useParams();
  // define state variables to store the forum data
  const [forum, setForum] = useState(null);

  // on mount, fetch the forum data
  useEffect(() => {
    try {
      // make an API call to fetch the forum data
      (async () => {
        const response = await axios.get(
          `http://127.0.0.1:8080/api/get_forum/${forumId}/`
        );
        if (!response || !response.data) {
          throw new Error("Invalid server response");
        }
        // store the forum data in state
        setForum(response.data);
      })();
    } catch (error) {
      console.error("Failed to fetch forum", error);
    }
  }, [forumId]);

  if (!forum) {
    return <div>Loading...</div>;
  }
  // copilot ^_^

  return (
    <div className="row text-center mt-3">
      <h1>{forum.title}</h1>
    </div>
  );
};
