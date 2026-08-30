'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { api, Student, StudyLog, Message } from '@/lib/api'

export default function StudentDetail() {
  const params = useParams()
  const id = Number(params.id)
  const [student, setStudent] = useState<Student | null>(null)
  const [studyLogs, setStudyLogs] = useState<StudyLog[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')

  useEffect(() => {
    if (id) {
      api.getStudent(id).then(setStudent)
      api.getStudyLogs(id).then(setStudyLogs)
      api.getMessages(id).then(setMessages)
    }
  }, [id])

  const handleSendMessage = async () => {
    if (newMessage.trim() && id) {
      await api.sendMessage(id, newMessage)
      setNewMessage('')
      api.getMessages(id).then(setMessages)
    }
  }

  if (!student) return <div className="p-8">در حال بارگذاری...</div>

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">{student.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">اطلاعات شخصی</h2>
            <p><strong>رشته:</strong> {student.field}</p>
            <p><strong>سال کنکور:</strong> {student.target_year}</p>
            <p><strong>تاریخ عضویت:</strong> {new Date(student.created_at).toLocaleDateString('fa-IR')}</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">آخرین فعالیت‌ها</h2>
            {studyLogs.slice(0, 5).map(log => (
              <div key={log.id} className="border-b py-2">
                <span>{log.subject}: {log.hours} ساعت</span>
                <span className="text-gray-500 mr-2">
                  {new Date(log.date).toLocaleDateString('fa-IR')}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">ارسال پیام</h2>
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="flex-1 border rounded px-4 py-2"
              placeholder="پیام خود را بنویسید..."
            />
            <button
              onClick={handleSendMessage}
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
            >
              ارسال
            </button>
          </div>

          <div className="max-h-64 overflow-y-auto">
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`p-3 rounded mb-2 ${
                  msg.sender === 'consultant'
                    ? 'bg-blue-100 ml-auto'
                    : 'bg-gray-100'
                }`}
              >
                <p>{msg.content}</p>
                <small className="text-gray-500">
                  {new Date(msg.created_at).toLocaleString('fa-IR')}
                </small>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
