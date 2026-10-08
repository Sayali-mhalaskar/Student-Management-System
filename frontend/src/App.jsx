import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'
function App() {

  const [students, setStudents] = useState([])
  const [id, setId] = useState('')
  const [name, setName] = useState('')
  const [course, setCourse] = useState('')
  const [isEdit, setIsEdit] = useState(false)

  

  async function getAllStudents() {
    const response = await axios.get('http://127.0.0.1:8000/students')
    setStudents(response.data)
  }

  useEffect(() => {
    getAllStudents()
  }, [])

  function storeId(event) {
    setId(event.target.value)
  }
  function storeName(event) {
    setName(event.target.value)
  }
  function storeCourse(event) {
    setCourse(event.target.value)
  }

  async function sendData() {
    if(isEdit === false) {
      const response = await axios.post('http://127.0.0.1:8000/students', {
        id: id,
        name: name,
        course: course
      })
      window.alert(response.data.detail)
    } else {
      const response = await axios.put(`http://127.0.0.1:8000/students/${id}`, {
        id: id,
        name: name,
        course: course
      })
      window.alert(response.data.detail)
    }
  }

  function edit(student) {
    setId(student.id)
    setName(student.name)
    setCourse(student.course)
    setIsEdit(true)
  }

  return(
    <div className="container">
      <h1>Student Management System</h1>
      <form className='student-form'>
        <input type="number" placeholder='ID' onChange={storeId} value={id} />
        <input type="text" placeholder='Name' onChange={storeName} value={name} />
        <input type="text" placeholder='Course' onChange={storeCourse} value={course} />
        <button onClick={sendData}>{ isEdit ? 'Update' : 'Submit' }</button>
      </form>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Course</th>
            <th>Edit</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          { students.map((student) => {
            return(
              <tr key={student.id}>
                <td>{student.id}</td>
                <td>{student.name}</td>
                <td>{student.course}</td>
                <td><button className='edit-btn' onClick={() => {edit(student)}}>Edit</button></td>
                <td><button className='delete-btn'>Delete</button></td>
              </tr>
            )
          }) }
        </tbody>
      </table>
    </div>
  )
}

export default App