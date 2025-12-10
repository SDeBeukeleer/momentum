"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Activity,
  Flame,
  Clock,
  MapPin,
  Plus,
  Trash2,
  Calendar,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { ActivityLog } from "@prisma/client";

interface ActivityViewProps {
  initialLogs: ActivityLog[];
}

const activityTypes = [
  { value: "running", label: "Running", icon: "🏃", color: "bg-red-100 text-red-700" },
  { value: "cycling", label: "Cycling", icon: "🚴", color: "bg-blue-100 text-blue-700" },
  { value: "swimming", label: "Swimming", icon: "🏊", color: "bg-cyan-100 text-cyan-700" },
  { value: "gym", label: "Gym / Weights", icon: "🏋️", color: "bg-purple-100 text-purple-700" },
  { value: "yoga", label: "Yoga", icon: "🧘", color: "bg-pink-100 text-pink-700" },
  { value: "hiking", label: "Hiking", icon: "🥾", color: "bg-green-100 text-green-700" },
  { value: "walking", label: "Walking", icon: "🚶", color: "bg-emerald-100 text-emerald-700" },
  { value: "sports", label: "Sports", icon: "⚽", color: "bg-orange-100 text-orange-700" },
  { value: "other", label: "Other", icon: "🎯", color: "bg-slate-100 text-slate-700" },
];

export function ActivityView({ initialLogs }: ActivityViewProps) {
  const [logs, setLogs] = useState(initialLogs);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    activityType: "",
    duration: "",
    distance: "",
    notes: "",
  });

  // Calculate stats
  const thisWeekLogs = logs.filter((log) => {
    const logDate = new Date(log.date);
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    return logDate >= weekAgo;
  });

  const totalDurationThisWeek = thisWeekLogs.reduce(
    (sum, log) => sum + (log.duration || 0),
    0
  );

  const totalDistanceThisWeek = thisWeekLogs.reduce(
    (sum, log) => sum + (log.distance || 0),
    0
  );

  // Calculate active days streak
  const getActiveDaysStreak = () => {
    if (logs.length === 0) return 0;

    const sortedDates = [...new Set(
      logs.map((log) => {
        const d = new Date(log.date);
        return `${d.getUTCFullYear()}-${d.getUTCMonth()}-${d.getUTCDate()}`;
      })
    )].sort().reverse();

    let streak = 0;
    const today = new Date();
    let checkDate = new Date(Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()));

    for (let i = 0; i < 365; i++) {
      const dateKey = `${checkDate.getUTCFullYear()}-${checkDate.getUTCMonth()}-${checkDate.getUTCDate()}`;
      if (sortedDates.includes(dateKey)) {
        streak++;
        checkDate = new Date(checkDate.getTime() - 24 * 60 * 60 * 1000);
      } else {
        break;
      }
    }

    return streak;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.activityType || loading) return;

    setLoading(true);

    try {
      const res = await fetch("/api/activities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          activityType: formData.activityType,
          duration: formData.duration ? parseInt(formData.duration) : null,
          distance: formData.distance ? parseFloat(formData.distance) : null,
          notes: formData.notes || null,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        toast.error(data.error || "Failed to log activity");
        return;
      }

      const newLog = await res.json();
      setLogs((prev) => [newLog, ...prev]);
      setFormData({ activityType: "", duration: "", distance: "", notes: "" });
      setDialogOpen(false);
      toast.success("Activity logged!");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      const res = await fetch(`/api/activities?id=${id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        setLogs((prev) => prev.filter((log) => log.id !== id));
        toast.success("Activity deleted");
      }
    } catch {
      toast.error("Failed to delete");
    }
  };

  const getActivityConfig = (type: string) => {
    return activityTypes.find((a) => a.value === type) || activityTypes[activityTypes.length - 1];
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center">
            <Activity className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Activities</h1>
            <p className="text-slate-600">Track your workouts and sports</p>
          </div>
        </div>

        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button className="gap-2">
              <Plus className="h-4 w-4" />
              Log Activity
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Log Activity</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label>Activity Type</Label>
                <Select
                  value={formData.activityType}
                  onValueChange={(value) =>
                    setFormData((prev) => ({ ...prev, activityType: value }))
                  }
                >
                  <SelectTrigger className="mt-1">
                    <SelectValue placeholder="Select activity" />
                  </SelectTrigger>
                  <SelectContent>
                    {activityTypes.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        <span className="flex items-center gap-2">
                          <span>{type.icon}</span>
                          <span>{type.label}</span>
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="duration">Duration (minutes)</Label>
                  <Input
                    id="duration"
                    type="number"
                    placeholder="30"
                    value={formData.duration}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, duration: e.target.value }))
                    }
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="distance">Distance (km)</Label>
                  <Input
                    id="distance"
                    type="number"
                    step="0.1"
                    placeholder="5.0"
                    value={formData.distance}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, distance: e.target.value }))
                    }
                    className="mt-1"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="notes">Notes (optional)</Label>
                <Input
                  id="notes"
                  placeholder="How did it go?"
                  value={formData.notes}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, notes: e.target.value }))
                  }
                  className="mt-1"
                />
              </div>

              <Button type="submit" className="w-full" disabled={loading || !formData.activityType}>
                {loading ? "Saving..." : "Log Activity"}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <Flame className="h-5 w-5 mx-auto text-orange-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {getActiveDaysStreak()}
          </div>
          <div className="text-xs text-slate-500">Day Streak</div>
        </Card>

        <Card className="p-4 text-center">
          <Activity className="h-5 w-5 mx-auto text-blue-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {thisWeekLogs.length}
          </div>
          <div className="text-xs text-slate-500">This Week</div>
        </Card>

        <Card className="p-4 text-center">
          <Clock className="h-5 w-5 mx-auto text-purple-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {totalDurationThisWeek}
          </div>
          <div className="text-xs text-slate-500">Minutes</div>
        </Card>

        <Card className="p-4 text-center">
          <MapPin className="h-5 w-5 mx-auto text-green-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {totalDistanceThisWeek.toFixed(1)}
          </div>
          <div className="text-xs text-slate-500">km</div>
        </Card>
      </div>

      {/* Recent Activities */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Recent Activities</h3>
        {logs.length === 0 ? (
          <p className="text-slate-500 text-center py-8">
            No activities logged yet. Start tracking your workouts!
          </p>
        ) : (
          <div className="space-y-3">
            <AnimatePresence>
              {logs.slice(0, 20).map((log) => {
                const config = getActivityConfig(log.activityType);
                return (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -100 }}
                    className="flex items-center gap-4 p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors"
                  >
                    <div className="text-2xl">{config.icon}</div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{config.label}</span>
                        <Badge variant="secondary" className={config.color}>
                          {new Date(log.date).toLocaleDateString("en-US", {
                            weekday: "short",
                            month: "short",
                            day: "numeric",
                          })}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-3 mt-1 text-sm text-slate-500">
                        {log.duration && (
                          <span className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {log.duration} min
                          </span>
                        )}
                        {log.distance && (
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {log.distance} km
                          </span>
                        )}
                        {log.notes && (
                          <span className="truncate">{log.notes}</span>
                        )}
                      </div>
                    </div>
                    <Button
                      size="icon"
                      variant="ghost"
                      className="h-8 w-8 text-slate-400 hover:text-red-500"
                      onClick={() => handleDelete(log.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
      </Card>
    </div>
  );
}
