import { useEffect, useState } from 'react'
import { Card, Table, Button, Tag, Space, Modal, Form, Input, DatePicker, Select, Switch, message } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import { injuryApi } from '../services/api'

const { Option } = Select
const { TextArea } = Input

const InjuryRecordsPage = () => {
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
      const response = await injuryApi.getRecords()
      setRecords(response.data)
    } catch (error) {
      message.error('Failed to load injury records')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingRecord(null)
    form.resetFields()
    form.setFieldsValue({ is_ongoing: true, is_recurring: false })
    setModalVisible(true)
  }

  const handleEdit = (record: any) => {
    setEditingRecord(record)
    form.setFieldsValue({
      ...record,
      start_date: dayjs(record.start_date),
      end_date: record.end_date ? dayjs(record.end_date) : null
    })
    setModalVisible(true)
  }

  const handleDelete = async (id: number) => {
    try {
      await injuryApi.deleteRecord(id)
      message.success('Injury record deleted')
      fetchRecords()
    } catch (error) {
      message.error('Failed to delete record')
    }
  }

  const handleSubmit = async (values: any) => {
    try {
      const data = {
        ...values,
        start_date: values.start_date.toISOString(),
        end_date: values.end_date ? values.end_date.toISOString() : null
      }

      if (editingRecord) {
        await injuryApi.updateRecord(editingRecord.id, data)
        message.success('Injury record updated')
      } else {
        await injuryApi.createRecord(data)
        message.success('Injury record created')
      }
      setModalVisible(false)
      fetchRecords()
    } catch (error) {
      message.error('Failed to save record')
    }
  }

  const columns = [
    {
      title: 'Type',
      dataIndex: 'injury_type',
      key: 'injury_type',
      render: (type: string) => <Tag color="red">{type}</Tag>
    },
    {
      title: 'Body Part',
      dataIndex: 'body_part',
      key: 'body_part'
    },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => {
        const colors: Record<string, string> = {
          mild: 'green',
          moderate: 'orange',
          severe: 'red'
        }
        return <Tag color={colors[severity] || 'default'}>{severity}</Tag>
      }
    },
    {
      title: 'Start Date',
      dataIndex: 'start_date',
      key: 'start_date',
      render: (date: string) => dayjs(date).format('YYYY-MM-DD')
    },
    {
      title: 'Status',
      key: 'status',
      render: (_: any, record: any) => (
        <Space>
          {record.is_ongoing && <Tag color="red">Ongoing</Tag>}
          {record.is_recurring && <Tag color="orange">Recurring</Tag>}
          {!record.is_ongoing && <Tag color="green">Recovered</Tag>}
        </Space>
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
        <h1>Injury Records</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          Add Injury Record
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
        title={editingRecord ? 'Edit Injury Record' : 'Add Injury Record'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        width={600}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="injury_type" label="Injury Type" rules={[{ required: true }]}>
            <Select placeholder="Select injury type">
              <Option value="strain">Strain (拉伤)</Option>
              <Option value="sprain">Sprain (扭伤)</Option>
              <Option value="inflammation">Inflammation (炎症)</Option>
              <Option value="fracture">Fracture (骨折)</Option>
              <Option value="tendinitis">Tendinitis (肌腱炎)</Option>
              <Option value="other">Other (其他)</Option>
            </Select>
          </Form.Item>
          <Form.Item name="body_part" label="Body Part" rules={[{ required: true }]}>
            <Select placeholder="Select body part">
              <Option value="knee">Knee (膝盖)</Option>
              <Option value="ankle">Ankle (脚踝)</Option>
              <Option value="shoulder">Shoulder (肩膀)</Option>
              <Option value="wrist">Wrist (手腕)</Option>
              <Option value="elbow">Elbow (手肘)</Option>
              <Option value="back">Back (背部)</Option>
              <Option value="hip">Hip (髋部)</Option>
              <Option value="hamstring">Hamstring (腘绳肌)</Option>
              <Option value="quadriceps">Quadriceps (股四头肌)</Option>
              <Option value="calf">Calf (小腿)</Option>
              <Option value="achilles">Achilles (跟腱)</Option>
              <Option value="other">Other (其他)</Option>
            </Select>
          </Form.Item>
          <Form.Item name="severity" label="Severity" rules={[{ required: true }]}>
            <Select placeholder="Select severity">
              <Option value="mild">Mild (轻度)</Option>
              <Option value="moderate">Moderate (中度)</Option>
              <Option value="severe">Severe (重度)</Option>
            </Select>
          </Form.Item>
          <Form.Item name="start_date" label="Start Date" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="end_date" label="End Date (leave empty if ongoing)">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="is_ongoing" label="Ongoing" valuePropName="checked">
            <Switch />
          </Form.Item>
          <Form.Item name="is_recurring" label="Recurring Injury" valuePropName="checked">
            <Switch />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <TextArea rows={3} placeholder="Describe the injury..." />
          </Form.Item>
          <Form.Item name="treatment" label="Treatment">
            <TextArea rows={3} placeholder="Describe the treatment..." />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default InjuryRecordsPage
