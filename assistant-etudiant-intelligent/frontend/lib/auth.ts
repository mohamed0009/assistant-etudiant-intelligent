// Authentication utilities and types
export interface User {
  id: string
  email: string
  name: string
  role: "student" | "admin"
  studentId?: string
  department?: string
  createdAt: Date
}

export interface AuthState {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
}

// Mock authentication - in production, replace with real auth service
export const mockUsers: User[] = [
  {
    id: "1",
    email: "admin@univ-tech.fr",
    name: "Administrateur Système",
    role: "admin",
    createdAt: new Date(),
  },
  {
    id: "2",
    email: "etudiant@univ-tech.fr",
    name: "Marie Dupont",
    role: "student",
    studentId: "ET2024001",
    department: "Informatique",
    createdAt: new Date(),
  },
]

export const authenticateUser = async (email: string, password: string): Promise<User | null> => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Mock authentication logic
  const user = mockUsers.find((u) => u.email === email)
  if (user && password === "password123") {
    return user
  }
  return null
}

export const getCurrentUser = (): User | null => {
  if (typeof window === "undefined") return null
  const userData = localStorage.getItem("currentUser")
  return userData ? JSON.parse(userData) : null
}

export const setCurrentUser = (user: User | null) => {
  if (typeof window === "undefined") return
  if (user) {
    localStorage.setItem("currentUser", JSON.stringify(user))
  } else {
    localStorage.removeItem("currentUser")
  }
}
