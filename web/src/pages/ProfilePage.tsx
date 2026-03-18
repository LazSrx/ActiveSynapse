import { useEffect, useState } from 'react'
import { Card, Form, Button, Select, DatePicker, InputNumber, message, Spin } from 'antd'
import { SaveOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import { userApi } from '../services/api'
import { useAuthStore } from '../stores/authStore'

const { Option } = Select

const ProfilePage = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const { user } = useAuthStore()

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      setLoading(true)
      const response = await userApi.getProfile()
      const profile = response.data
      if (profile) {
        form.setFieldsValue({
          ...profile,
          birth_date: profile.birth_date ? dayjs(profile.birth_date) : null
        })
      }
    } catch (error) {
      message.error('Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      setSaving(true)
      const data = {
        ...values,
        birth_date: values.birth_date ? values.birth_date.toISOString() : null
      }
      await userApi.updateProfile(data)
      message.success('Profile updated successfully')
    } catch (error) {
      message.error('Failed to update profile')
    } finally {
      setSaving(false)
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
      <h1 style={{ marginBottom: 24 }}>My Profile</h1>
      
      <Card title="Basic Information" style={{ marginBottom: 24 }}>
        <p><strong>Username:</strong> {user?.username}</p>
        <p><strong>Email:</strong> {user?.email}</p>
      </Card>

      <Card title="Sports Profile">
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item name="height_cm" label="Height (cm)">
            <InputNumber min={50} max={300} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="weight_kg" label="Weight (kg)">
            <InputNumber min={20} max={300} step={0.1} style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="birth_date" label="Birth Date">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="gender" label="Gender">
            <Select placeholder="Select gender">
              <Option value="male">Male</Option>
              <Option value="female">Female</Option>
              <Option value="other">Other</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="sport_level" label="Sport Level">
            <Select placeholder="Select your sport level">
              <Option value="beginner">Beginner (初学者)</Option>
              <Option value="intermediate">Intermediate (进阶)</Option>
              <Option value="advanced">Advanced (高级)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="sport_goals" label="Sport Goals">
            <Select mode="multiple" placeholder="Select your goals">
              <Option value="weight_loss">Weight Loss (减脂)</Option>
              <Option value="muscle_gain">Muscle Gain (增肌)</Option>
              <Option value="endurance">Improve Endurance (提升耐力)</Option>
              <Option value="performance">Performance (提升成绩)</Option>
              <Option value="health">General Health (保持健康)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="preferred_sports" label="Preferred Sports">
            <Select mode="multiple" placeholder="Select your preferred sports">
              <Option value="running">Running (跑步)</Option>
              <Option value="badminton">Badminton (羽毛球)</Option>
              <Option value="strength">Strength Training (力量训练)</Option>
              <Option value="swimming">Swimming (游泳)</Option>
              <Option value="cycling">Cycling (骑行)</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={saving}>
              Save Profile
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default ProfilePage
