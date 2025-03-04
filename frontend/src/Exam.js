import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './exam.css';
import Webcam from 'react-webcam';
import axios from 'axios';

function Exam() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const [showFullScreenButton, setShowFullScreenButton] = useState(false);
  const [showCameraOverlay, setShowCameraOverlay] = useState(true);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [showFullScreenAlert, setShowFullScreenAlert] = useState(false);
  const [showTabSwitchAlert, setShowTabSwitchAlert] = useState(false);
  const [timer, setTimer] = useState(0);
  const [timerRunning, setTimerRunning] = useState(true);
  const [timeUpAlert, setTimeUpAlert] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const [unansweredCount, setUnansweredCount] = useState(0);
  const [score, setScore] = useState(0);
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);
  const user = JSON.parse(localStorage.getItem('user'));
  const [questions, setQuestions] = useState([]);

  let countSwitch = 3;
  const [switchCount, setSwitchCount] = useState(4);

  const timePerQuestion = 60; // Time per question in seconds

  const webcamRef = useRef(null);
  const [warning, setWarning] = useState('');

  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    try {
      const response = await axios.post('http://127.0.0.1:8000/detect/', {
        image: imageSrc,
        id: user.id,
      });
      if (response.data.warning) {
        setWarning(response.data.warning);
        setTimeout(() => {
          setWarning('');
        }, 3000); // Clear the warning after 3 seconds
      }
    } catch (error) {
      console.error('Error sending image to backend', error);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      capture();
    }, 1000); // Capture every second

    return () => clearInterval(interval);
    // eslint-disable-next-line
  }, []);

  // Start recording the video and audio
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoRef.current.srcObject = stream;
    videoRef.current.muted = true;
    mediaRecorder.current = new MediaRecorder(stream);
    mediaRecorder.current.ondataavailable = (e) => {
      chunks.current.push(e.data);
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  // Fetch the quiz data from API
  useEffect(() => {
    async function fetchQuizData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/get_quiz/');
        const data = await response.json();
        if (data.status) {
          // Map the response to match the expected format
          const fetchedQuestions = data.data.map((q) => ({
            questionText: q.question,
            answers: q.answers.map((a, index) => ({
              id: `A${index + 1}`,
              label: a.answer,
              isCorrect: a.is_correct,
            })),
            correctAnswer: q.answers.find((a) => a.is_correct).answer,
          }));
          setQuestions(fetchedQuestions);
          setTimer(fetchedQuestions.length * timePerQuestion); // Set timer based on number of questions
        }
      } catch (error) {
        console.error('Error fetching quiz data:', error);
      }
    }
    fetchQuizData();
  }, []);

  useEffect(() => {
    function checkFullScreen() {
      if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
        setShowFullScreenAlert(true);
        setShowFullScreenButton(true);
      }
    }

    function handleVisibilityChange() {
      if (document.hidden) {
        setShowTabSwitchAlert(true);
        setSwitchCount((prevCount) => prevCount - 1);
        countSwitch--;

        if (countSwitch === 0) {
          handleLogout();
        }
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('fullscreenchange', checkFullScreen);
    document.addEventListener('mozfullscreenchange', checkFullScreen);
    document.addEventListener('webkitfullscreenchange', checkFullScreen);
    document.addEventListener('msfullscreenchange', checkFullScreen);

    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      document.removeEventListener('fullscreenchange', checkFullScreen);
      document.removeEventListener('mozfullscreenchange', checkFullScreen);
      document.removeEventListener('webkitfullscreenchange', checkFullScreen);
      document.removeEventListener('msfullscreenchange', checkFullScreen);
    };
    // eslint-disable-next-line
  }, [navigate, countSwitch]);

  useEffect(() => {
    // Request camera access and display feed
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play();
            setIsCameraOn(true); // Set camera status to on
            setShowCameraOverlay(false); // Hide camera overlay
          };
        }
      } catch (err) {
        console.error('Error accessing the camera: ', err);
        // Handle error (e.g., show a message to the user)
        setIsCameraOn(false);
      }
    }

    setupCamera();
  }, [isCameraOn]);

  // Start recording when the component mounts
  useEffect(() => {
    startRecording();
  }, [recording]);


  useEffect(() => {
    if (timerRunning) {
      const interval = setInterval(() => {
        setTimer((prevTime) => {
          if (prevTime <= 0) {
            clearInterval(interval);
            setTimeUpAlert(true);
            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timerRunning]);

  function goFullScreen() {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    }
    setShowFullScreenButton(false); // Hide the button once full-screen mode is activated
  }

  function exitFullScreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
    setShowFullScreenButton(true);
  }

  useEffect(() => {
    // Calculate and set the timer based on the number of questions
    const totalQuestions = questions.length;
    setTimer(totalQuestions * timePerQuestion);
  }, [questions.length]);

  const handleNextClick = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePreviousClick = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleAnswerChange = (event) => {
    const { name, value } = event.target;
    setSelectedAnswers({ ...selectedAnswers, [name]: value });
  };

  const handleGoBack = () => {
    // Reset all states to go back to the initial question and allow the user to retry
    setCurrentQuestionIndex(0);
    setSelectedAnswers({});
    setQuizSubmitted(false);
    setShowWarning(false);
    setScore(0);
    setUnansweredCount(0);
    setTimer(questions.length * timePerQuestion);
    setTimerRunning(true);
  };

  function handleFullScreenButtonClick() {
    setShowFullScreenAlert(false); // Hide the full-screen alert
    goFullScreen(); // Enter full-screen mode
  }
  
  const calculateScore = async () => {
    let score = 0;

    questions.forEach((question, index) => {
        if (selectedAnswers[`q${index + 1}`] === question.correctAnswer) {
            score += 1;
        }
    });

    setScore(score);
    setQuizSubmitted(true);
    setTimerRunning(false);
  };
  
  const handleSubmit = (event) => {
    if (event) event.preventDefault();
    if (timer <= 0) {
      // If time has run out, directly submit without showing the warning
      calculateScore();
    } else {
      // Calculate unanswered questions and show warning
      const unansweredQuestions = questions.filter(
        (q, index) => !selectedAnswers[`q${index + 1}`]
      ).length;

      if (unansweredQuestions > 0) {
        setUnansweredCount(unansweredQuestions);
        setShowWarning(true);
      } else {
        calculateScore();
      }
    }
  };

  const handleConfirmSubmit = () => {
    setShowWarning(false);
    calculateScore();
  };  

  const timeUpSubmit = () => {
    calculateScore();
    setTimeUpAlert(false);
  }

  const submitMarks = async () => {
    const user = JSON.parse(localStorage.getItem("user"));
    const email = user ? user.email : null;

    if (!email) {
        console.error("User is not logged in");
        return;
    }

    try {
        const response = await axios.put("http://127.0.0.1:8000/students/update_marks/", {
            email: email,
            marks_obtained: score
        });
        console.log("Score submitted successfully:", response.data);
    } catch (error) {
        console.error("Error submitting score:", error.response.data);
    }
  };

  const submitVideo = async () => {
    // Stop the recording
    mediaRecorder.current.stop();
  
    mediaRecorder.current.onstop = async () => {
      const blob = new Blob(chunks.current, { type: 'video/mp4' });
      const formData = new FormData();
      formData.append('video', blob, 'recording.mp4');
  
      // Attach user information (e.g., email) to the formData
      formData.append('email', user.email); 
  
      try {
        // Send the recorded video to Django backend
        const response = await fetch('http://127.0.0.1:8000/students/upload_video/', {
          method: 'POST',
          body: formData,
        });
  
        if (response.ok) {
          console.log("Video uploaded successfully");
        } else {
          console.error("Error uploading video:", response.statusText);
        }
      } catch (error) {
        console.error("Error in video upload:", error);
      }

      // Clear the chunks for the next recording
      chunks.current = [];
      setRecording(false);
    };
  };

  const handleLogout = () => {
    submitMarks();   
    submitVideo();
    // Clear the session (localStorage or sessionStorage)
    localStorage.removeItem('user');
    
    // Navigate to the login page
    navigate('/');
    exitFullScreen();
    window.location.reload();
  };

  return (
    <div>
      <div className="timer">
      <span style={{ fontWeight: 'bold' }}>Time Remaining : </span> {String(Math.floor(timer / 60)).padStart(2, '0')}:{String(timer % 60).padStart(2, '0')}
      </div> 
      {showCameraOverlay && (
        <div className="camera-overlay">
          <p>Please enable your camera to start the exam.</p>
        </div>
      )}
      <Webcam audio={false} ref={webcamRef} mirrored={false} screenshotFormat="image/jpeg" className="camera-feed" /> {/* for real time warning message generation */}
      {warning &&
        <div className="modal-overlay">
          <div className="modal">
            <p className="warning-text">
              <strong style={{ color: 'red' }}>
                {warning}
              </strong>
            </p>
          </div>
        </div>
      }
      <video ref={videoRef} autoPlay muted className="camera-feed-hidden" />  {/* for screen recording for video storage and at last for audio processing */}
      {showFullScreenAlert && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="warning-text">
              <i className="fas fa-exclamation-triangle"></i>
              <strong>
                Warning: You have exited full-screen mode. Please return to full-screen mode immediately!
              </strong>
            </div>
            <div className="modal-buttons">
              {showFullScreenButton && (
                <button onClick={handleFullScreenButtonClick} className="fullscreen-button">
                  <i className="fas fa-expand"></i>
                  Enter Full-Screen
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {showTabSwitchAlert && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="warning-text">
              <i className="fas fa-exclamation-circle"></i>
              <strong>
                Warning: You are not allowed to switch tabs. If you switch tabs {switchCount} more time(s), you will be eliminated from the exam!
              </strong>
            </div>
            <div className="modal-buttons">
              <button onClick={() => setShowTabSwitchAlert(false)} className="fullscreen-button">
                <i className="fas fa-check"></i>
                Understood
              </button>
            </div>
          </div>
        </div>
      )}

      {timeUpAlert && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="warning-text" style={{ background: '#FEF3C7', borderColor: '#FDE68A' }}>
              <i className="fas fa-clock" style={{ color: '#D97706' }}></i>
              <strong style={{ color: '#92400E' }}>
                Time is up! Your exam will be submitted automatically.
              </strong>
            </div>
            <div className="modal-buttons">
              <button onClick={timeUpSubmit} className="fullscreen-button">
                <i className="fas fa-paper-plane"></i>
                Submit Quiz
              </button>
            </div>
          </div>
        </div>
      )}


      <div className="App">
        {!quizSubmitted && !timeUpAlert ? (
          <form onSubmit={handleSubmit}>
            <p>{questions[currentQuestionIndex]?.questionText}</p>
            {questions[currentQuestionIndex]?.answers.map((answer) => (
              <div key={answer.id} className='answers'>
                <input
                  type="radio"
                  id={answer.id}
                  name={`q${currentQuestionIndex + 1}`}
                  value={answer.label}
                  onChange={handleAnswerChange}
                  checked={selectedAnswers[`q${currentQuestionIndex + 1}`] === answer.label}
                />
                <label htmlFor={answer.id}>{answer.label}</label>
              </div>
            ))}

            <div className="navigation-buttons">
              {currentQuestionIndex > 0 && (
                <button type="button" onClick={handlePreviousClick}>
                  Previous
                </button>
              )}

              {currentQuestionIndex < questions.length - 1 && (
                <button type="button" onClick={handleNextClick}>
                  Next
                </button>
              )}

              {currentQuestionIndex === questions.length - 1 && (
                <button type="submit">Submit</button>
              )}
            </div>
          </form>
        ) : (
          <div className="results">
            <h2>Quiz Results</h2>
            <p>
              You scored <span>{score}</span> out of <span>{questions.length}</span>
            </p>
            <div className="modal-buttons">
              <button onClick={handleGoBack}>Retry</button>
              <button onClick={handleLogout}>Logout</button>
            </div>
          </div>
        )}

        {showWarning && (
          <div className="modal-overlay">
            <div className="modal">
              <p className="warning-text">
                <strong style={{ color: 'red' }}>
                  Warning: You have {unansweredCount} unanswered question(s).
                </strong>
                <br />
                Would you like to submit the quiz anyway?
              </p>
              <div className="modal-buttons">
                <button onClick={handleConfirmSubmit}>Yes</button>
                <button onClick={() => setShowWarning(false)}>Return</button>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default Exam;