'use client'

import { useEffect, useState } from 'react'
import { api, Student, StudentStats } from '@/lib/api'
import Link from 'next/link'

export default function Dashboard() {
  const [students, setStudents] = useState<Student[]>([])
  const [stats, setStats] = useState<{ [key: number]: StudentStats }>({})

  useEffect(() => {
    api.getStudents().then(async (data) => {
      setStudents(data)
      for (const student of data) {
        const studentStats = await api.getStudentStats(student.id)
        setStats(prev => ({ ...prev, [student.id]: studentStats }))
      }
    })
  }, [])

  const totalStudents = students.length
  const totalHours = Object.values(stats).reduce((sum, s) => sum + s.total_hours, 0)
  const todayHours = Object.values(stats).reduce((sum, s) => sum + s.today_hours, 0)

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">داشبورد مدیریت</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-600">تعداد دانش‌آموزان</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">{totalStudents}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-600">کل ساعت مطالعه</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">{totalHours}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-600">ساعت مطالعه امروز</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">{todayHours}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">آخرین وضعیت دانش‌آموزان</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-right py-3 px-4">نام</th>
                  <th className="text-right py-3 px-4">رشته</th>
                  <th className="text-right py-3 px-4">کنکور</th>
                  <th className="text-right py-3 px-4">کل ساعت</th>
                  <th className="text-right py-3 px-4">امروز</th>
                  <th className="text-right py-3 px-4">عملیات</th>
                </tr>
              </thead>
              <tbody>
                {students.map(student => (
                  <tr key={student.id} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4">{student.name}</td>
                    <td className="py-3 px-4">{student.field}</td>
                    <td className="py-3 px-4">{student.target_year}</td>
                    <td className="py-3 px-4">{stats[student.id]?.total_hours || 0}</td>
                    <td className="py-3 px-4">{stats[student.id]?.today_hours || 0}</td>
                    <td className="py-3 px-4">
                      <Link
                        href={`/students/${student.id}`}
                        className="text-blue-600 hover:underline"
                      >
                        جزئیات
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
