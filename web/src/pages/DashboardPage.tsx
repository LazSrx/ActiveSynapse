import { useEffect, useState } from 'react'
import { Card, Row, Col, Statistic, Spin, message } from 'antd'
import { TrophyOutlined, FireOutlined, ClockCircleOutlined, MedicineBoxOutlined } from '@ant-design/icons'
import { sportApi, injuryApi } from '../services/api'

const DashboardPage = () => {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<any>(null)
  const [weeklySummary, setWeeklySummary] = useState<any>(null)
  const [injurySummary, setInjurySummary] = useState<any>(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [statsRes, weeklyRes, injuryRes] = await Promise.all([
        sportApi.getStatistics({ days: 30 }),
        sportApi.getWeeklySummary(),
        injuryApi.getSummary()
      ])
      
      setStats(statsRes.data)
      setWeeklySummary(weeklyRes.data)
      setInjurySummary(injuryRes.data)
    } catch (error) {
      message.error('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div>
      <h1 style={{ marginBottom: 24 }}>Dashboard</h1>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Activities (30 days)"
              value={stats?.total_activities || 0}
              prefix={<TrophyOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Duration (hours)"
              value={Math.round((stats?.total_duration_minutes || 0) / 60 * 10) / 10}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Calories Burned"
              value={stats?.total_calories || 0}
              prefix={<FireOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Ongoing Injuries"
              value={injurySummary?.ongoing_injuries || 0}
              prefix={<MedicineBoxOutlined />}
              valueStyle={{ color: (injurySummary?.ongoing_injuries || 0) > 0 ? '#cf1322' : '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      {stats?.running && (
        <Card title="Running Statistics (30 days)" style={{ marginTop: 24 }}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={8}>
              <Statistic title="Total Distance" value={stats.running.total_distance_km} suffix="km" />
            </Col>
            <Col xs={24} sm={8}>
              <Statistic title="Average Pace" value={stats.running.avg_pace_min_per_km} suffix="min/km" />
            </Col>
            <Col xs={24} sm={8}>
              <Statistic title="Average Heart Rate" value={stats.running.avg_heart_rate} suffix="bpm" />
            </Col>
          </Row>
        </Card>
      )}

      {weeklySummary && (
        <Card title="This Week's Activity" style={{ marginTop: 24 }}>
          <Row gutter={[16, 16]}>
            <Col span={24}>
              <p>Week: {weeklySummary.week_start} to {weeklySummary.week_end}</p>
              <p>Total Activities: {weeklySummary.total_activities}</p>
            </Col>
          </Row>
        </Card>
      )}
    </div>
  )
}

export default DashboardPage
