import { QueryClient, QueryClientProvider, useMutation } from "@tanstack/react-query"
import { sendFn } from "./service/api"
import { useRef } from "react"



const queryClient = new QueryClient()

function App() {
  return <QueryClientProvider client={queryClient}>
    <Chatbot />
  </QueryClientProvider>
}



function Chatbot() {
  const inputRef = useRef<any>(null)
  const langRef = useRef<any>(null)

  const {mutate, data} = useMutation({
    mutationFn: sendFn
  })

  const handleSend = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    mutate({
      txt: inputRef.current.value,
      lang: langRef.current.value
    })
  }

  return (
    <>
      {JSON.stringify(data)}
      <form onSubmit={handleSend}>
        <input type="text" ref={inputRef} placeholder="User" />
        <input type="text" ref={langRef} placeholder="Language" />
        <button>Send</button>
      </form>
    </>
  )
}

export default App
