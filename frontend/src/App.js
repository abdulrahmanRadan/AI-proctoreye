import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import AddStudent from "./students/AddStudent";
import StudentList from "./students/StudentList";
import CompareImage from "./components/CompareImage";

function Home() {
  return <h1>Welcome to Home Page</h1>;
}

function App() {
  return (
    <Router future={{ v7_relativeSplatPath: true, v7_startTransition: true }}>
      <div className="App">
        <nav className="bg-gray-800 p-4">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="text-white hover:text-gray-400">
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/add-student"
                className="text-white hover:text-gray-400"
              >
                Add Student
              </Link>
            </li>
            <li>
              <Link to="/students" className="text-white hover:text-gray-400">
                Student List
              </Link>
            </li>
            <li>
              <Link
                to="/compare-image"
                className="text-white hover:text-gray-400"
              >
                Compare Image
              </Link>
            </li>
          </ul>
        </nav>
        <div className="p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add-student" element={<AddStudent />} />
            <Route path="/students" element={<StudentList />} />
            <Route path="/compare-image" element={<CompareImage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;