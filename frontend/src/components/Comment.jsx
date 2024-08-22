import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { Link } from "react-router-dom";

export const Comment = ({ comment, loggedUser }) => {
  // define state variable to store the likes count
  const [likesCount, setLikesCount] = useState(comment.likes_count);

  // define a handler for when the thumbs up icon is clicked
  const handleLikeCount = async () => {
    try {
      // make an API call to update the like count
      const response = await axios.post(
        `http://127.0.0.1:8080/api/update_comment_likes/${comment.id}/`
      );
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // update the likes count in state
      setLikesCount(response.data.likes_count);
    } catch (error) {
      console.error("Failed to update comment like count", error);
    }
  };
  // define a handler for deleting a comment
  const handleDeleteComment = async (commentId) => {
    try {
      // make an API call to delete the comment
      const response = await axios.post(
        `http://127.0.0.1:8080/api/delete_comment/${comment.id}/`
      );
      if (!response || !response.data) {
        throw new Error("Invalid server response");
      }
      // refresh the page
      window.location.reload(); // copilot ^_^
    } catch (error) {
      console.error("Failed to delete comment", error);
    }
  };

  return (
    <div className="row m-3 d-flex gap-2 align-items-center justify-content-center">
      <div className="col-md-6 card shadow p-2">
        <div className="d-flex justify-content-between align-items-center">
          <div className="d-flex gap-2 align-items-center">
            <img
              src={comment.picture}
              alt="profile"
              className="comment_profile_picture"
            />
            <p className="m-0">{comment.author}</p>
          </div>
          <p className="m-0">{comment.timestamp}</p>
        </div>
        <p className="mt-2">{comment.content}</p>
        <div className="d-flex gap-2 align-items-center">
          <span>
            <FontAwesomeIcon
              icon={faThumbsUp}
              onClick={handleLikeCount}
              className="me-2"
            />
            {likesCount}
          </span>
          {/* if the comment author is the logged in user, display the delete link */}
          {loggedUser === comment.author && (
            <Link onClick={() => handleDeleteComment(comment.id)}>Delete</Link>
          )}
        </div>
      </div>
    </div>
  );
};
