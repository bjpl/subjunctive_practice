"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/hooks/use-redux";
import { useResetProgressMutation } from "@/store/api/progressApi";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { ArrowLeft, Save, Trash2, Bell, BookOpen, Palette, Accessibility } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function SettingsPage() {
  const router = useRouter();
  const { toast } = useToast();
  const { isAuthenticated, user } = useAppSelector((state) => state.auth);
  const [resetProgress, { isLoading: isResetting }] = useResetProgressMutation();

  const [settings, setSettings] = useState({
    dailyGoal: 10,
    autoAdvance: true,
    showHints: true,
    showExplanations: true,
    emailNotifications: true,
    pushNotifications: false,
    streakReminders: true,
    fontSize: "medium" as "small" | "medium" | "large",
    theme: "system" as "light" | "dark" | "system",
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  const handleSaveSettings = () => {
    // In a real app, save to backend
    toast({
      title: "Settings Saved",
      description: "Your preferences have been updated successfully.",
    });
  };

  const handleResetProgress = async () => {
    try {
      await resetProgress().unwrap();
      toast({
        title: "Progress Reset",
        description: "Your learning progress has been reset successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to reset progress. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold">Settings</h1>
            <p className="mt-2 text-muted-foreground">
              Customize your learning experience
            </p>
          </div>
          <Button variant="outline" onClick={() => router.push("/dashboard")}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </div>

        {/* Account Information */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
            <CardDescription>Your account details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Username</Label>
              <Input value={user?.username || ""} disabled className="mt-1" />
            </div>
            <div>
              <Label>Email</Label>
              <Input value={user?.email || ""} disabled className="mt-1" />
            </div>
          </CardContent>
        </Card>

        {/* Practice Settings */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              Practice Settings
            </CardTitle>
            <CardDescription>Configure your practice sessions</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="dailyGoal">Daily Exercise Goal</Label>
              <Input
                id="dailyGoal"
                type="number"
                value={settings.dailyGoal}
                onChange={(e) =>
                  setSettings({ ...settings, dailyGoal: parseInt(e.target.value) })
                }
                min={1}
                max={100}
                className="mt-1"
              />
              <p className="mt-1 text-xs text-muted-foreground">
                Number of exercises to complete each day
              </p>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Auto-advance to next exercise</Label>
                <p className="text-xs text-muted-foreground">
                  Automatically move to next exercise after answering
                </p>
              </div>
              <Button
                variant={settings.autoAdvance ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({ ...settings, autoAdvance: !settings.autoAdvance })
                }
              >
                {settings.autoAdvance ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Show hints</Label>
                <p className="text-xs text-muted-foreground">
                  Display hint buttons during practice
                </p>
              </div>
              <Button
                variant={settings.showHints ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({ ...settings, showHints: !settings.showHints })
                }
              >
                {settings.showHints ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Show explanations</Label>
                <p className="text-xs text-muted-foreground">
                  Display detailed explanations after each answer
                </p>
              </div>
              <Button
                variant={settings.showExplanations ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({ ...settings, showExplanations: !settings.showExplanations })
                }
              >
                {settings.showExplanations ? "On" : "Off"}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notifications
            </CardTitle>
            <CardDescription>Manage how you receive updates</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>Email notifications</Label>
                <p className="text-xs text-muted-foreground">
                  Receive progress updates via email
                </p>
              </div>
              <Button
                variant={settings.emailNotifications ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({
                    ...settings,
                    emailNotifications: !settings.emailNotifications,
                  })
                }
              >
                {settings.emailNotifications ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Push notifications</Label>
                <p className="text-xs text-muted-foreground">
                  Receive browser notifications
                </p>
              </div>
              <Button
                variant={settings.pushNotifications ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({
                    ...settings,
                    pushNotifications: !settings.pushNotifications,
                  })
                }
              >
                {settings.pushNotifications ? "On" : "Off"}
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Streak reminders</Label>
                <p className="text-xs text-muted-foreground">
                  Get reminded to maintain your streak
                </p>
              </div>
              <Button
                variant={settings.streakReminders ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  setSettings({
                    ...settings,
                    streakReminders: !settings.streakReminders,
                  })
                }
              >
                {settings.streakReminders ? "On" : "Off"}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Appearance Settings */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Palette className="h-5 w-5" />
              Appearance
            </CardTitle>
            <CardDescription>Customize the look and feel</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="theme">Theme</Label>
              <Select
                value={settings.theme}
                onValueChange={(value: "light" | "dark" | "system") =>
                  setSettings({ ...settings, theme: value })
                }
              >
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="light">Light</SelectItem>
                  <SelectItem value="dark">Dark</SelectItem>
                  <SelectItem value="system">System</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Accessibility Settings */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Accessibility className="h-5 w-5" />
              Accessibility
            </CardTitle>
            <CardDescription>Make the app more comfortable to use</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="fontSize">Font Size</Label>
              <Select
                value={settings.fontSize}
                onValueChange={(value: "small" | "medium" | "large") =>
                  setSettings({ ...settings, fontSize: value })
                }
              >
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="small">Small</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="large">Large</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-destructive">
              <Trash2 className="h-5 w-5" />
              Danger Zone
            </CardTitle>
            <CardDescription>Irreversible actions</CardDescription>
          </CardHeader>
          <CardContent>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive" disabled={isResetting}>
                  <Trash2 className="mr-2 h-4 w-4" />
                  Reset All Progress
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete all your
                    progress, statistics, and achievements.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={handleResetProgress} className="bg-destructive">
                    Yes, reset my progress
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="mt-6 flex justify-end">
          <Button onClick={handleSaveSettings} size="lg">
            <Save className="mr-2 h-4 w-4" />
            Save Settings
          </Button>
        </div>
      </div>
    </div>
  );
}
