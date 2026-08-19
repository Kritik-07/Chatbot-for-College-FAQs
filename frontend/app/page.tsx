'use client'

import { FormEvent, useState } from 'react'
import {
  Bot,
  Check,
  CircleHelp,
  FileText,
  Menu,
  Paperclip,
  Plus,
  Send,
  Sparkles,
  Trash2,
  UserRound,
} from 'lucide-react'

const initialMessages = [
  {
    id: 1,
    role: 'bot' as const,
    time: '10:30 AM',
    content: (
      <>
        <p>Hello! I&apos;m your T. JIT FAQ assistant.</p>
        <p className="mt-2">Ask me anything about admissions, courses, fees, placements, hostel, academics and more.</p>
      </>
    ),
  },
]

export default function Page() {
  const [messages, setMessages] = useState(initialMessages)
  const [question, setQuestion] = useState('')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  async function submitQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!question.trim()) return

    const text = question.trim()

    setMessages((current) => [
      ...current,
      {
        id: Date.now(),
        role: 'user' as const,
        time: 'Just now',
        content: <p>{text}</p>,
      },
    ])

    setQuestion('')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
        }),
      })

      const data = await response.json()

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'bot' as const,
          time: 'Just now',
          content: (
            <>
              <p>{data.response || 'Sorry, I could not find an answer.'}</p>
              {data.sources?.length > 0 && (
                <div className="mt-4 border-t border-border/70 pt-3">
                  <div className="mb-2 flex items-center gap-2 text-[11px] font-semibold text-foreground">
                    <FileText className="size-3.5 text-primary" />
                    Sources
                  </div>
                  {data.sources.map((source: any, index: number) => (
                    <p key={index} className="text-[11px] text-primary">
                      + {source.question}
                    </p>
                  ))}
                </div>
              )}
            </>
          ),
        },
      ])
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: 'bot' as const,
          time: 'Just now',
          content: <p>Sorry, I couldn&apos;t connect to the chatbot server.</p>,
        },
      ])
    }
  }

  function clearChat() {
    setMessages([])
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="flex min-h-screen">
        <aside className={`${sidebarOpen ? 'flex' : 'hidden'} fixed inset-y-0 left-0 z-20 w-[238px] flex-col border-r border-border bg-card px-4 py-5 shadow-xl md:static md:flex md:shadow-none`}>
          <div className="flex items-start gap-3 px-2">
            <div className="flex size-9 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-card shadow-sm">
              <img src="/tjohn_logo.jpg" alt="T. John Institute of Technology logo" className="size-full object-contain" />
            </div>
            <div>
              <p className="font-serif text-[15px] font-bold leading-tight text-primary">T. John Institute</p>
              <p className="font-serif text-[15px] font-bold leading-tight text-primary">of Technology</p>
              <p className="mt-1 text-[9px] uppercase tracking-[0.16em] text-muted-foreground">Knowledge assistant</p>
            </div>
          </div>
          <button className="mt-9 flex items-center gap-2 rounded-md bg-primary px-3 py-2 text-left text-xs font-medium text-primary-foreground shadow-sm transition hover:opacity-90" onClick={() => setMessages(initialMessages)}>
            <Plus className="size-3.5" /> New Chat
          </button>
          <div className="mt-7 rounded-xl border border-border bg-muted/40 p-3">
            <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-primary">About the college</p>
            <p className="mt-2 text-[10px] leading-relaxed text-muted-foreground">T. John Institute of Technology is committed to quality technical education, innovation, and career-ready learning.</p>
            <div className="mt-3 flex flex-col gap-2 text-[10px] text-muted-foreground">
              <span><strong className="font-semibold text-foreground">Programs:</strong> Engineering, Technology &amp; Management</span>
              <span><strong className="font-semibold text-foreground">Focus:</strong> Academics, research &amp; placements</span>
              <span><strong className="font-semibold text-foreground">Location:</strong> Bengaluru, Karnataka</span>
            </div>
          </div>
          <div className="mt-auto border-t border-border pt-4">
            <p className="px-2 text-[10px] leading-relaxed text-muted-foreground">Ask questions about admissions, courses, fees, placements, and campus life.</p>
            <button className="mt-4 flex items-center gap-2 px-2 text-[11px] text-muted-foreground hover:text-foreground"><CircleHelp className="size-3.5" /> Help center</button>
          </div>
        </aside>

        {sidebarOpen && <button aria-label="Close navigation" className="fixed inset-0 z-10 bg-foreground/20 md:hidden" onClick={() => setSidebarOpen(false)} />}

        <section className="flex min-w-0 flex-1 flex-col bg-card/70">
          <header className="flex min-h-[76px] items-center justify-between border-b border-border bg-card px-5 py-4 md:px-8">
            <div className="flex items-center gap-3">
              <button aria-label="Open navigation" className="rounded-md p-1.5 text-muted-foreground hover:bg-muted md:hidden" onClick={() => setSidebarOpen(true)}><Menu className="size-5" /></button>
              <div>
                <h1 className="font-serif text-lg font-bold tracking-tight text-primary md:text-xl">College FAQ Chatbot</h1>
                <p className="mt-1 text-[10px] text-muted-foreground">Ask questions about T. John Institute of Technology</p>
              </div>
            </div>
            <button onClick={clearChat} className="flex items-center gap-1.5 rounded-md border border-border px-3 py-2 text-[10px] font-medium text-primary transition hover:bg-muted"><Trash2 className="size-3.5" /> Clear Chat</button>
          </header>

          <div className="relative flex-1 overflow-y-auto bg-[radial-gradient(circle_at_50%_0%,hsl(var(--primary)/0.04),transparent_45%)] px-4 pb-36 pt-7 md:px-12 lg:px-24">
            <div className="mx-auto flex max-w-[760px] flex-col gap-5">
              {messages.length === 0 && <div className="flex flex-col items-center justify-center py-24 text-center"><Sparkles className="size-8 text-primary/50" /><p className="mt-3 font-serif text-lg font-semibold text-primary">Start a new conversation</p><p className="mt-1 text-xs text-muted-foreground">Ask anything about life at T. JIT.</p></div>}
              {messages.map((message) => (
                <div key={message.id} className={`flex items-start gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {message.role === 'bot' && <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full border border-primary/20 bg-primary text-primary-foreground shadow-sm"><Bot className="size-4" /></div>}
                  <div className={`${message.role === 'user' ? 'max-w-[78%] rounded-xl rounded-tr-sm bg-accent text-accent-foreground' : 'max-w-[540px] rounded-xl rounded-tl-sm border border-border bg-card text-card-foreground shadow-sm'} px-4 py-3 text-[11px] leading-relaxed`}>
                    {message.content}
                    <div className={`mt-2 flex items-center justify-end gap-1 text-[9px] ${message.role === 'user' ? 'text-primary/60' : 'text-muted-foreground'}`}>{message.time}{message.role === 'user' && <Check className="size-3" />}</div>
                  </div>
                  {message.role === 'user' && <div className="mt-1 flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary"><UserRound className="size-4" /></div>}
                </div>
              ))}
            </div>
          </div>

          <div className="fixed bottom-0 left-0 right-0 border-t border-border bg-card/95 px-4 py-4 backdrop-blur md:static md:px-12 lg:px-24">
            <form onSubmit={submitQuestion} className="mx-auto flex max-w-[760px] items-center gap-2 rounded-lg border border-border bg-background p-1.5 shadow-sm focus-within:ring-2 focus-within:ring-ring/30">
              <button type="button" aria-label="Attach a file" className="rounded-md p-2 text-muted-foreground hover:bg-muted"><Paperclip className="size-4" /></button>
              <input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a question about T. JIT..." className="min-w-0 flex-1 bg-transparent px-1 text-xs outline-none placeholder:text-muted-foreground" />
              <button type="submit" aria-label="Send question" className="flex size-8 items-center justify-center rounded-md bg-primary text-primary-foreground transition hover:opacity-90"><Send className="size-3.5" /></button>
            </form>
            <p className="mx-auto mt-2 hidden max-w-[760px] text-center text-[9px] text-muted-foreground sm:block">T. JIT FAQ assistant can make mistakes. Verify important information with the institute.</p>
          </div>
        </section>
      </div>
    </main>
  )
}