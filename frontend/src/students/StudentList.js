import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";

const StudentList = () => {
  const [students, setStudents] = useState([]);
  const [successMessage, setSuccessMessage] = useState(null);
  const location = useLocation();

  const fetchStudents = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/students");
      // console.log(response.data);
      setStudents(response.data);
    } catch (error) {
      console.error("Failed to fetch students", error);
    }
  };

  // إعداد الرسالة الأولية من التنقل
  useEffect(() => {
    if (location.state?.message) {
      setSuccessMessage(location.state.message);

      // تعيين مؤقت لإخفاء الرسالة بعد 5 ثوانٍ
      const timer = setTimeout(() => {
        setSuccessMessage(null);
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [location.state?.message]);

  useEffect(() => {
    fetchStudents();
  }, []);

  return (
    <div className=" w-full mx-auto h-full p-6 bg-gray-50 rounded-lg shadow-md">
      {successMessage && (
        <div className="bg-green-100 text-green-700 p-4 mb-4 rounded-md">
          {successMessage}
        </div>
      )}

      <h2 className="text-2xl font-bold mb-4">Student List</h2>
      <ul className="space-y-4">
        {students.map((student) => (
          <li
            key={student.StudentID}
            className="p-4 border-b border-gray-200 flex items-start"
          >
            <img
              src={student.ImagePath}
              alt={student.Number}
              className="w-16 h-16 rounded-full mr-4"
            />
            <div className="flex flex-1 gap-4 border-spacing-2 justify-between text-center items-center font-semibold ">
              <p>
                <strong>Number:</strong> {student.Number}
              </p>
              <p>
                <strong>College:</strong> {student.College}
              </p>
              <p>
                <strong>Level:</strong> {student.Level}
              </p>
              <p>
                <strong>Specialization:</strong> {student.Specialization}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StudentList;
