import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { PostsModal } from "./PostsModal";

export const Forum = () => {
  // get the form id from the URL
  const { forumId } = useParams();
  // define state variables to store the forum data
  const [forum, setForum] = useState(null);
  const [posts, setPosts] = useState([]);
  // define state variable that will control the visibility of the modal
  const [showModal, setShowModal] = useState(false);
  // define handlers for showing and hiding the modal
  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  // define a handler for submitting the form
  const handleSubmit = async (title, content) => {
    try {
      // create a FormData object to send the form data
      const formData = new FormData();
      formData.append("title", title);
      formData.append("content", content);
      formData.append("forum_id", forumId);
      // make an API call to create a new post
      const response = await axios.post(
        "http://127.0.0.1:8080/api/create_post/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      handleCloseModal();
    } catch (error) {
      console.error("Failed to create post", error);
    }
  };
  // useNavigate is a hook that allows us to navigate to different pages
  const navigate = useNavigate();
  // define a handler for clicking on a post
  const handlePostClick = (postId) => {
    // navigate to the post page
    navigate(`/townhall/forum/${forumId}/post/${postId}`);
  };

  // on mount, fetch the forum data
  useEffect(() => {
    try {
      // make an API call to fetch the forum data
      (async () => {
        const forumResponse = await axios.get(
          `http://127.0.0.1:8080/api/get_forum/${forumId}/`
        );
        if (!forumResponse || !forumResponse.data) {
          throw new Error("Invalid server response");
        }
        // store the forum data in state
        setForum(forumResponse.data);
        const postsResponse = await axios.get(
          `http://127.0.0.1:8080/api/get_posts/${forumId}/`
        );
        if (!postsResponse || !postsResponse.data) {
          throw new Error("Invalid server response");
        }
        // store the posts data in state
        setPosts(postsResponse.data);
      })();
    } catch (error) {
      console.error("Failed to fetch forum", error);
    }
  }, [forumId]);

  if (!forum) {
    return <div>Loading...</div>;
    // copilot ^_^
  }

  return (
    <>
      <div className="row text-center mt-3">
        <h1>{forum.title}</h1>
      </div>
      {/* create post button */}
      <button className="button" onClick={handleShowModal}>
        Create Post
      </button>
      {/* list of posts */}
      {posts.length > 0 ? (
        posts.map((post, index) => (
          <div
            key={index}
            className="card my-2"
            onClick={() => handlePostClick(post.id)}
          >
            <div className="card-body">
              <h5 className="card-title">{post.title}</h5>
              <p className="card-text">
                {post.content.split(" ").splice(0, 10).join(" ")}...
              </p>
              <p className="card-text">
                created by: {post.author} at {post.timestamp}
              </p>
            </div>
          </div>
        ))
      ) : (
        <div className="row text-center mt-3">
          <h2>No available posts at the moment...</h2>
        </div>
      )}
      {/* modal to create posts */}
      <PostsModal
        show={showModal}
        handleClose={handleCloseModal}
        onSubmit={handleSubmit}
      />
    </>
  );
};
