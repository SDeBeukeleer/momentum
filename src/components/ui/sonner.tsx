"use client"

import {
  CircleCheckIcon,
  InfoIcon,
  Loader2Icon,
  OctagonXIcon,
  TriangleAlertIcon,
} from "lucide-react"
import { useTheme } from "next-themes"
import { Toaster as Sonner, type ToasterProps } from "sonner"

const Toaster = ({ ...props }: ToasterProps) => {
  const { theme = "system" } = useTheme()

  return (
    <Sonner
      theme={theme as ToasterProps["theme"]}
      className="toaster group"
      icons={{
        success: <CircleCheckIcon className="size-4" />,
        info: <InfoIcon className="size-4" />,
        warning: <TriangleAlertIcon className="size-4" />,
        error: <OctagonXIcon className="size-4" />,
        loading: <Loader2Icon className="size-4 animate-spin" />,
      }}
      style={
        {
          "--normal-bg": "#ffffff",
          "--normal-text": "#1e293b",
          "--normal-border": "#e2e8f0",
          "--success-bg": "#f0fdf4",
          "--success-text": "#166534",
          "--success-border": "#bbf7d0",
          "--error-bg": "#fef2f2",
          "--error-text": "#991b1b",
          "--error-border": "#fecaca",
          "--border-radius": "0.75rem",
        } as React.CSSProperties
      }
      toastOptions={{
        classNames: {
          toast: "bg-white border-slate-200 shadow-lg",
          title: "text-slate-900 font-medium",
          description: "text-slate-500",
          success: "!bg-emerald-50 !border-emerald-200 !text-emerald-800 [&_[data-title]]:!text-emerald-800 [&_[data-description]]:!text-emerald-600",
          error: "!bg-red-50 !border-red-200 !text-red-800 [&_[data-title]]:!text-red-800 [&_[data-description]]:!text-red-600",
        },
      }}
      {...props}
    />
  )
}

export { Toaster }
