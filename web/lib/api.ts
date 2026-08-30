const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Student {
  id: number
  telegram_id: number
  name: string
  field: string
  target_year: number
  created_at: string
}

export interface StudyLog {
  id: number
  student_id: number
  subject: string
  hours: number
  date: string
}

export interface Schedule {
  id: number
  student_id: number
  day_of_week: number
  subject: string
  hours: number
  description?: string
}

export interface Message {
  id: number
  student_id: number
  sender: string
  content: string
  created_at: string
}

export interface StudentStats {
  student: Student
  total_hours: number
  today_hours: number
}

export const api = {
  async getStudents(): Promise<Student[]> {
    const res = await fetch(`${API_URL}/students/`)
    return res.json()
  },

  async getStudent(id: number): Promise<Student> {
    const res = await fetch(`${API_URL}/students/${id}`)
    return res.json()
  },

  async getStudentStats(id: number): Promise<StudentStats> {
    const res = await fetch(`${API_URL}/students/${id}/stats`)
    return res.json()
  },

  async getStudyLogs(studentId: number): Promise<StudyLog[]> {
    const res = await fetch(`${API_URL}/study/${studentId}`)
    return res.json()
  },

  async getSchedule(studentId: number): Promise<Schedule[]> {
    const res = await fetch(`${API_URL}/schedule/${studentId}`)
    return res.json()
  },

  async getMessages(studentId: number): Promise<Message[]> {
    const res = await fetch(`${API_URL}/messages/${studentId}`)
    return res.json()
  },

  async sendMessage(studentId: number, content: string): Promise<Message> {
    const res = await fetch(`${API_URL}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: studentId,
        sender: 'consultant',
        content
      })
    })
    return res.json()
  },

  async createSchedule(schedule: Omit<Schedule, 'id'>): Promise<Schedule> {
    const res = await fetch(`${API_URL}/schedule/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(schedule)
    })
    return res.json()
  },

  async deleteSchedule(id: number): Promise<void> {
    await fetch(`${API_URL}/schedule/${id}`, { method: 'DELETE' })
  }
}
