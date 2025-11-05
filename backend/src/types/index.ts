// User Types
export interface User {
  id: number;
  username: string;
  email: string;
  password_hash: string;
  full_name: string;
  role: 'admin' | 'manager' | 'teacher';
  phone?: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name: string;
  role: 'admin' | 'manager' | 'teacher';
  phone?: string;
}

// Student Types
export interface Student {
  id: number;
  student_number: string;
  first_name: string;
  last_name: string;
  class_id?: number;
  date_of_birth?: Date;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface StudentWithClass extends Student {
  class_name?: string;
  grade_level?: number;
}

// Parent Types
export interface Parent {
  id: number;
  first_name: string;
  last_name: string;
  phone: string;
  email?: string;
  relationship?: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

// Class Types
export interface Class {
  id: number;
  name: string;
  grade_level: number;
  section: string;
  academic_year: string;
  teacher_id?: number;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

// Message Types
export interface Message {
  id: number;
  sender_id: number;
  message_type: 'SMS' | 'WhatsApp';
  recipient_type: string;
  subject?: string;
  content: string;
  recipient_count: number;
  sent_count: number;
  failed_count: number;
  status: 'pending' | 'sending' | 'sent' | 'failed' | 'scheduled';
  scheduled_at?: Date;
  sent_at?: Date;
  created_at: Date;
  updated_at: Date;
}

export interface MessageCreate {
  sender_id: number;
  message_type: 'SMS' | 'WhatsApp';
  recipient_type: string;
  subject?: string;
  content: string;
  scheduled_at?: Date;
  recipients: MessageRecipientCreate[];
}

export interface MessageRecipient {
  id: number;
  message_id: number;
  recipient_name: string;
  phone: string;
  personalized_content: string;
  status: 'pending' | 'sent' | 'failed' | 'delivered';
  provider_message_id?: string;
  sent_at?: Date;
  delivered_at?: Date;
  error_message?: string;
  created_at: Date;
  updated_at: Date;
}

export interface MessageRecipientCreate {
  recipient_name: string;
  phone: string;
  personalized_content: string;
}

// Message Template Types
export interface MessageTemplate {
  id: number;
  name: string;
  category?: string;
  content: string;
  variables?: string[];
  created_by: number;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

// Staff Types
export interface Staff {
  id: number;
  user_id?: number;
  first_name: string;
  last_name: string;
  phone: string;
  email?: string;
  position?: string;
  department?: string;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

// Contact Types
export interface Contact {
  id: number;
  name: string;
  phone: string;
  email?: string;
  notes?: string;
  tags?: string[];
  created_by: number;
  is_active: boolean;
  created_at: Date;
  updated_at: Date;
}

// Provider Settings Types
export interface ProviderSettings {
  id: number;
  provider_name: string;
  provider_type: 'SMS' | 'WhatsApp';
  api_key?: string;
  api_secret?: string;
  sender_id?: string;
  webhook_url?: string;
  is_active: boolean;
  is_default: boolean;
  settings?: Record<string, any>;
  created_at: Date;
  updated_at: Date;
}

// Attendance Types
export interface Attendance {
  id: number;
  student_id: number;
  date: Date;
  status: 'present' | 'absent' | 'late' | 'excused';
  notes?: string;
  notified: boolean;
  created_by: number;
  created_at: Date;
  updated_at: Date;
}

// Exam Result Types
export interface ExamResult {
  id: number;
  student_id: number;
  exam_name: string;
  subject?: string;
  score: number;
  max_score: number;
  exam_date?: Date;
  notified: boolean;
  created_by: number;
  created_at: Date;
  updated_at: Date;
}

// Meeting Types
export interface Meeting {
  id: number;
  title: string;
  description?: string;
  meeting_date: Date;
  location?: string;
  organizer_id: number;
  target_group?: string;
  notified: boolean;
  created_at: Date;
  updated_at: Date;
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
  errors?: any[];
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}

// Auth Types
export interface AuthToken {
  userId: number;
  username: string;
  role: string;
  iat: number;
  exp: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email: string;
    full_name: string;
    role: string;
  };
}

// Bulk Message Types
export interface BulkMessageRequest {
  message_type: 'SMS' | 'WhatsApp';
  content: string;
  recipients: {
    type: 'class' | 'student_numbers' | 'parents' | 'staff' | 'custom';
    class_ids?: number[];
    student_numbers?: string[];
    phone_numbers?: string[];
    staff_ids?: number[];
  };
  scheduled_at?: string;
  template_id?: number;
}

// Report Types
export interface MessageReport {
  total_messages: number;
  sent_messages: number;
  failed_messages: number;
  pending_messages: number;
  total_recipients: number;
  sent_recipients: number;
  failed_recipients: number;
  delivery_rate: number;
}

export interface UsageReport {
  period: string;
  sms_sent: number;
  whatsapp_sent: number;
  total_cost: number;
  top_senders: Array<{
    user_name: string;
    message_count: number;
  }>;
}
