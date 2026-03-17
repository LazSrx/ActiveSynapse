import { useEffect, useState } from 'react'
import { Card, Table, Button, Tag, Space, Modal, Form, Input, DatePicker, Select, InputNumber, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import { sportApi } from '../services/api'

const { Option } = Select

const SportRecordsPage = () => {
  const [records, setRecords] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingRecord, setEditingRecord] = useState<any>(null)
  const [form] = Form.useForm()

  useEffect(() => {
    fetchRecords()
  }, [])

  const fetchRecords = async () => {
    setLoading(true)
    try {
      const response = await sportApi.getRecords()
      setRecords(response.data)
    } catch (error) {
      message.error('Failed to load records')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingRecord(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (record: any) => {
    setEditingRecord(record)
    form.setFieldsValue({
      ...record,
      record_date: dayjs(record.record_date)
    })
    setModalVisible(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await sportApi.deleteRecord(id)
      message.success('Record deleted')
      fetchRecords()
    } catch (error) {
      message.error('Failed to delete record')
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      const data = {
        ...values,
        record_date: values.record_date.toISOString()
      }

      if (editingRecord) {
        await sportApi.updateRecord(editingRecord.id, data)
        message.success('Record updated')
      } else {
        await sportApi.createRecord(data)
        message.success('Record created')
      }
      setModalVisible(false)
      fetchRecords()
    } catch (error) {
      message.error('Failed to save record')
    }
  }

  const columns = [
    {
      title: 'Date',
      dataIndex: 'record_date',
      key: 'record_date',
      render: (date: string) => dayjs(date).format('YYYY-MM-DD HH:mm')
    },
    {
      title: 'Type',
      dataIndex: 'sport_type',
      key: 'sport_type',
      render: (type: string) => (
        <Tag color={type === 'running' ? 'blue' : 'green'}>
          {type === 'running' ? 'Running' : 'Badminton'}
        </Tag>
      )
    },
    {
      title: 'Duration (min)',
      dataIndex: 'duration_minutes',
      key: 'duration_minutes'
    },
    {
      title: 'Calories',
      dataIndex: 'calories_burned',
      key: 'calories_burned'
    },
    {
      title: 'Source',
      dataIndex: 'source',
      key: 'source',
      render: (source: string) => (
        <Tag color={source === 'coros' ? 'purple' : 'default'}>
          {source === 'coros' ? 'COROS' : 'Manual'}
        </Tag>
      )
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: any) => (
        <Space>
          <Button icon={<EditOutlined />} onClick={() => handleEdit(record)} />
          <Button icon={<DeleteOutlined />} danger onClick={() => handleDelete(record.id)} />
        </Space>
      )
    }
  ]

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h1>Sport Records</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          Add Record
        </Button>
      </div>

      <Card>
        <Table
          dataSource={records}
          columns={columns}
          rowKey="id"
          loading={loading}
        />
      </Card>

      <Modal
        title={editingRecord ? 'Edit Record' : 'Add Record'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="sport_type" label="Sport Type" rules={[{ required: true }]}>
            <Select>
              <Option value="running">Running</Option>
              <Option value="badminton">Badminton</Option>
            </Select>
          </Form.Item>
          <Form.Item name="record_date" label="Date" rules={[{ required: true }]}>
            <DatePicker showTime style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="duration_minutes" label="Duration (minutes)" rules={[{ required: true }]}>
            <InputNumber min={1} style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="calories_burned" label="Calories Burned">
            <InputNumber min={0} style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="notes" label="Notes">
            <Input.TextArea />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default SportRecordsPage
