def estimate_pose(frame, corners, ids, marker_size_cm=50, camera_matrix=None, dist_coeffs=None):
    """
    Estimate the pose of detected ArUco markers
    
    Args:
        image: Input image with detected markers
        corners: Corners of the detected markers
        ids: IDs of the detected markers
        marker_size_cm: Physical size of the marker in centimeters
        camera_matrix: Camera calibration matrix
        dist_coeffs: Distortion coefficients
    """
    # If camera parameters are not provided, use a default approximation
    if camera_matrix is None:
        # Approximate camera matrix for the input frame size
        h, w = frame.shape[:2]
        fx = fy = w / 2
        cx, cy = w/2, h/2
        camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)

    if dist_coeffs is None:
        # Assume no lens distortion
        dist_coeffs = np.zeros((5, 1), dtype=np.float32)

        # For each detected marker...
    if ids==None:
        return frame
    else:
      for i in range(len(ids)):
          # New API
          # Prepare objPoints for a square marker
          objPoints = np.array([
              [-marker_size_cm/2, marker_size_cm/2, 0],
              [marker_size_cm/2, marker_size_cm/2, 0],
              [marker_size_cm/2, -marker_size_cm/2, 0],
              [-marker_size_cm/2, -marker_size_cm/2, 0]
          ], dtype=np.float32)
          
          # Reshape corners for solvePnP
          imgPoints = corners[i].reshape((4, 2))
          
          # Estimate pose
          retval, rvec, tvec = cv2.solvePnP(objPoints, imgPoints, camera_matrix, dist_coeffs)

          # Draw the pose
          cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_size_cm/2)

          # Get rotation and translation info
          rotation_matrix, _ = cv2.Rodrigues(rvec)
          distance = np.linalg.norm(tvec)

          # Print pose information
          print(f"Marker {ids[i][0]} position (x,y,z): {tvec}")
          print(f"Distance from camera: {distance} cm")

    return frame