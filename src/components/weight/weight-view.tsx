"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Scale,
  TrendingDown,
  TrendingUp,
  Minus,
  Target,
  Calendar,
  Pencil,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { WeightLog } from "@prisma/client";

interface WeightViewProps {
  initialLogs: WeightLog[];
  goalWeight?: number;
}

export function WeightView({ initialLogs, goalWeight: initialGoalWeight }: WeightViewProps) {
  const [logs, setLogs] = useState(initialLogs);
  const [weight, setWeight] = useState("");
  const [loading, setLoading] = useState(false);
  const [goalWeight, setGoalWeight] = useState(initialGoalWeight);
  const [goalInput, setGoalInput] = useState(initialGoalWeight?.toString() || "");
  const [goalDialogOpen, setGoalDialogOpen] = useState(false);
  const [savingGoal, setSavingGoal] = useState(false);

  // Get current and previous weight for comparison
  const currentWeight = logs[0]?.weight;
  const previousWeight = logs[1]?.weight;
  const weightChange = currentWeight && previousWeight
    ? currentWeight - previousWeight
    : null;

  // Calculate stats
  const logsThisMonth = logs.filter((log) => {
    const logDate = new Date(log.date);
    const now = new Date();
    return (
      logDate.getMonth() === now.getMonth() &&
      logDate.getFullYear() === now.getFullYear()
    );
  });

  const startOfMonthWeight = logsThisMonth[logsThisMonth.length - 1]?.weight;
  const monthlyChange = currentWeight && startOfMonthWeight
    ? currentWeight - startOfMonthWeight
    : null;

  // Prepare chart data (reverse to show oldest first)
  const chartData = [...logs]
    .reverse()
    .slice(-30) // Last 30 entries
    .map((log) => ({
      date: new Date(log.date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      }),
      weight: log.weight,
    }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!weight || loading) return;

    setLoading(true);

    try {
      const res = await fetch("/api/weight", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ weight: parseFloat(weight) }),
      });

      if (!res.ok) {
        const data = await res.json();
        toast.error(data.error || "Failed to log weight");
        return;
      }

      const newLog = await res.json();

      // Update or add the log
      setLogs((prev) => {
        const existing = prev.findIndex((l) => l.id === newLog.id);
        if (existing >= 0) {
          const updated = [...prev];
          updated[existing] = newLog;
          return updated;
        }
        return [newLog, ...prev];
      });

      setWeight("");
      toast.success("Weight logged!");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (savingGoal) return;

    setSavingGoal(true);

    try {
      const res = await fetch("/api/weight/goal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goalWeight: goalInput ? parseFloat(goalInput) : null }),
      });

      if (!res.ok) {
        const data = await res.json();
        toast.error(data.error || "Failed to save goal weight");
        return;
      }

      setGoalWeight(goalInput ? parseFloat(goalInput) : undefined);
      setGoalDialogOpen(false);
      toast.success("Goal weight updated!");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setSavingGoal(false);
    }
  };

  const getTrendIcon = (change: number | null) => {
    if (change === null) return <Minus className="h-4 w-4 text-slate-400" />;
    if (change < 0) return <TrendingDown className="h-4 w-4 text-emerald-500" />;
    if (change > 0) return <TrendingUp className="h-4 w-4 text-amber-500" />;
    return <Minus className="h-4 w-4 text-slate-400" />;
  };

  const formatChange = (change: number | null) => {
    if (change === null) return "—";
    const sign = change > 0 ? "+" : "";
    return `${sign}${change.toFixed(1)} kg`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="h-12 w-12 rounded-xl bg-indigo-100 flex items-center justify-center">
          <Scale className="h-6 w-6 text-indigo-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'var(--font-fraunces)' }}>Weight Tracker</h1>
          <p className="text-slate-500">Track your progress over time</p>
        </div>
      </div>

      {/* Current Weight & Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <Scale className="h-5 w-5 mx-auto text-indigo-600 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {currentWeight ? `${currentWeight.toFixed(1)}` : "—"}
          </div>
          <div className="text-xs text-slate-500">Current (kg)</div>
        </Card>

        <Card className="p-4 text-center">
          <div className="mx-auto mb-2">{getTrendIcon(weightChange)}</div>
          <div className="text-lg font-bold text-slate-900">
            {formatChange(weightChange)}
          </div>
          <div className="text-xs text-slate-500">vs Last Entry</div>
        </Card>

        <Card className="p-4 text-center">
          <Calendar className="h-5 w-5 mx-auto text-amber-500 mb-2" />
          <div className="text-lg font-bold text-slate-900">
            {formatChange(monthlyChange)}
          </div>
          <div className="text-xs text-slate-500">This Month</div>
        </Card>

        <Dialog open={goalDialogOpen} onOpenChange={setGoalDialogOpen}>
          <DialogTrigger asChild>
            <Card className="p-4 text-center cursor-pointer hover:border-indigo-200 transition-all relative group">
              <Target className="h-5 w-5 mx-auto text-amber-500 mb-2" />
              <div className="text-lg font-bold text-slate-900">
                {goalWeight ? `${goalWeight} kg` : "Not set"}
              </div>
              <div className="text-xs text-slate-500">Goal Weight</div>
              <Pencil className="h-3 w-3 absolute top-2 right-2 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
            </Card>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="text-slate-900">Set Goal Weight</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSaveGoal} className="space-y-4">
              <div>
                <Label htmlFor="goalWeight" className="text-slate-700">Target Weight (kg)</Label>
                <Input
                  id="goalWeight"
                  type="number"
                  step="0.1"
                  placeholder="70.0"
                  value={goalInput}
                  onChange={(e) => setGoalInput(e.target.value)}
                  className="mt-1"
                />
                <p className="text-xs text-slate-500 mt-1">
                  Leave empty to clear your goal weight
                </p>
              </div>
              <div className="flex gap-3">
                <Button
                  type="button"
                  variant="outline"
                  className="flex-1"
                  onClick={() => setGoalDialogOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="flex-1 bg-indigo-600 hover:bg-indigo-700"
                  disabled={savingGoal}
                >
                  {savingGoal ? "Saving..." : "Save Goal"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Log Weight Form */}
      <Card className="p-4">
        <form onSubmit={handleSubmit} className="flex gap-3 items-end">
          <div className="flex-1">
            <Label htmlFor="weight" className="text-slate-700">Log Today&apos;s Weight</Label>
            <Input
              id="weight"
              type="number"
              step="0.1"
              placeholder="70.5"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              className="mt-1"
            />
          </div>
          <Button
            type="submit"
            disabled={loading || !weight}
            className="bg-indigo-600 hover:bg-indigo-700"
          >
            {loading ? "Saving..." : "Log Weight"}
          </Button>
        </form>
      </Card>

      {/* Weight Chart */}
      {chartData.length > 0 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-4 text-slate-900">Weight Trend</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.8} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 12 }}
                  stroke="#94a3b8"
                />
                <YAxis
                  domain={["dataMin - 2", "dataMax + 2"]}
                  tick={{ fontSize: 12 }}
                  stroke="#94a3b8"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e2e8f0",
                    borderRadius: "12px",
                    color: "#1e293b",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                />
                {goalWeight && (
                  <ReferenceLine
                    y={goalWeight}
                    stroke="#f59e0b"
                    strokeDasharray="5 5"
                    label={{ value: "Goal", fill: "#f59e0b", fontSize: 12 }}
                  />
                )}
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke="#4f46e5"
                  strokeWidth={2}
                  dot={{ fill: "#4f46e5", strokeWidth: 2 }}
                  activeDot={{ r: 6, fill: "#4f46e5" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {/* Recent Entries */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 text-slate-900">Recent Entries</h3>
        {logs.length === 0 ? (
          <p className="text-slate-500 text-center py-4">
            No weight entries yet. Start logging!
          </p>
        ) : (
          <div className="space-y-2">
            {logs.slice(0, 10).map((log, index) => {
              const prevLog = logs[index + 1];
              const change = prevLog ? log.weight - prevLog.weight : null;

              return (
                <motion.div
                  key={log.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0"
                >
                  <div className="flex items-center gap-3">
                    <div className="text-sm text-slate-500">
                      {new Date(log.date).toLocaleDateString("en-US", {
                        weekday: "short",
                        month: "short",
                        day: "numeric",
                      })}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-semibold text-slate-900">
                      {log.weight.toFixed(1)} kg
                    </span>
                    {change !== null && (
                      <span
                        className={`text-sm ${
                          change < 0
                            ? "text-emerald-500"
                            : change > 0
                            ? "text-amber-500"
                            : "text-slate-400"
                        }`}
                      >
                        {change > 0 ? "+" : ""}
                        {change.toFixed(1)}
                      </span>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </Card>
    </div>
  );
}
