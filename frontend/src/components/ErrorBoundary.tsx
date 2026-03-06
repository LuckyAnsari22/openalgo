import React, { Component, ErrorInfo, ReactNode } from 'react'
import { AlertTriangle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface Props {
    children?: ReactNode
}

interface State {
    hasError: boolean
    error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    }

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error }
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo)
    }

    private handleRetry = () => {
        this.setState({ hasError: false, error: undefined })
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="flex flex-col items-center justify-center min-h-[400px] p-6 text-center space-y-4">
                    <div className="bg-red-100 dark:bg-red-900/20 p-4 rounded-full">
                        <AlertTriangle className="h-10 w-10 text-red-600 dark:text-red-500" />
                    </div>
                    <h2 className="text-2xl font-bold tracking-tight">Something went wrong</h2>
                    <p className="text-muted-foreground max-w-md">
                        An unexpected error occurred while loading this page.
                        {this.state.error && (
                            <span className="block mt-2 text-sm opacity-80 break-words">
                                {this.state.error.message}
                            </span>
                        )}
                    </p>
                    <Button onClick={this.handleRetry} className="mt-4">
                        <RefreshCw className="mr-2 h-4 w-4" />
                        Try Again
                    </Button>
                </div>
            )
        }

        return this.props.children
    }
}
