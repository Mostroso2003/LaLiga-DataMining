"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PredictionResult {
  homeWin: number
  draw: number
  awayWin: number
}

const teams = [
  "Real Madrid",
  "Barcelona",
  "Atletico Madrid",
  "Sevilla",
  "Real Betis",
  "Villarreal",
  "Real Sociedad",
  "Athletic Bilbao",
  "Valencia",
  "Getafe",
]

export default function LaLigaPredictor() {
  const [homeTeam, setHomeTeam] = useState<string>("")
  const [awayTeam, setAwayTeam] = useState<string>("")
  const [results, setResults] = useState<PredictionResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam) return

    setIsLoading(true)

    // Simulate API call with random predictions
    setTimeout(() => {
      const homeWin = Math.floor(Math.random() * 60) + 20
      const draw = Math.floor(Math.random() * 40) + 15
      const awayWin = 100 - homeWin - draw

      setResults({ homeWin, draw, awayWin })
      setIsLoading(false)
    }, 1500)
  }

  const getHighestProbability = () => {
    if (!results) return null
    const max = Math.max(results.homeWin, results.draw, results.awayWin)
    if (max === results.homeWin) return "home"
    if (max === results.draw) return "draw"
    return "away"
  }

  const resetForm = () => {
    setHomeTeam("")
    setAwayTeam("")
    setResults(null)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Sistema Predictivo de Partidos de LaLiga
          </h1>
          <p className="text-gray-400 text-lg">
            Predice el resultado de los partidos de LaLiga con inteligencia artificial
          </p>
        </div>

        {/* Form Section */}
        <div className="max-w-2xl mx-auto mb-12">
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="text-center text-xl text-white">Selecciona los Equipos</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Equipo Local</label>
                  <Select value={homeTeam} onValueChange={setHomeTeam}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue placeholder="Selecciona equipo local" />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-700 border-gray-600">
                      {teams
                        .filter((team) => team !== awayTeam)
                        .map((team) => (
                          <SelectItem key={team} value={team} className="text-white hover:bg-gray-600">
                            {team}
                          </SelectItem>
                        ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Equipo Visitante</label>
                  <Select value={awayTeam} onValueChange={setAwayTeam}>
                    <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                      <SelectValue placeholder="Selecciona equipo visitante" />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-700 border-gray-600">
                      {teams
                        .filter((team) => team !== homeTeam)
                        .map((team) => (
                          <SelectItem key={team} value={team} className="text-white hover:bg-gray-600">
                            {team}
                          </SelectItem>
                        ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Button
                  onClick={handlePredict}
                  disabled={!homeTeam || !awayTeam || isLoading}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg font-semibold disabled:opacity-50"
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Analizando...
                    </div>
                  ) : (
                    "Predecir Resultado"
                  )}
                </Button>

                {results && (
                  <Button
                    onClick={resetForm}
                    variant="outline"
                    className="border-gray-600 text-gray-300 hover:bg-gray-700 px-6 py-3 bg-transparent"
                  >
                    Nueva Predicción
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Results Section */}
        {results && (
          <div className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-center mb-8 text-white">
              Predicción: {homeTeam} vs {awayTeam}
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Victoria Local */}
              <Card
                className={`${
                  getHighestProbability() === "home"
                    ? "bg-green-900 border-green-500 ring-2 ring-green-400"
                    : "bg-gray-800 border-gray-700"
                } transition-all duration-300`}
              >
                <CardHeader className="text-center pb-2">
                  <CardTitle
                    className={`text-lg ${getHighestProbability() === "home" ? "text-green-300" : "text-white"}`}
                  >
                    Victoria Local
                  </CardTitle>
                  <p className="text-sm text-gray-400">{homeTeam}</p>
                </CardHeader>
                <CardContent className="text-center">
                  <div
                    className={`text-4xl font-bold ${
                      getHighestProbability() === "home" ? "text-green-400" : "text-blue-400"
                    }`}
                  >
                    {results.homeWin}%
                  </div>
                  {getHighestProbability() === "home" && (
                    <p className="text-green-300 text-sm mt-2 font-semibold">Resultado más probable</p>
                  )}
                </CardContent>
              </Card>

              {/* Empate */}
              <Card
                className={`${
                  getHighestProbability() === "draw"
                    ? "bg-green-900 border-green-500 ring-2 ring-green-400"
                    : "bg-gray-800 border-gray-700"
                } transition-all duration-300`}
              >
                <CardHeader className="text-center pb-2">
                  <CardTitle
                    className={`text-lg ${getHighestProbability() === "draw" ? "text-green-300" : "text-white"}`}
                  >
                    Empate
                  </CardTitle>
                  <p className="text-sm text-gray-400">X</p>
                </CardHeader>
                <CardContent className="text-center">
                  <div
                    className={`text-4xl font-bold ${
                      getHighestProbability() === "draw" ? "text-green-400" : "text-yellow-400"
                    }`}
                  >
                    {results.draw}%
                  </div>
                  {getHighestProbability() === "draw" && (
                    <p className="text-green-300 text-sm mt-2 font-semibold">Resultado más probable</p>
                  )}
                </CardContent>
              </Card>

              {/* Victoria Visitante */}
              <Card
                className={`${
                  getHighestProbability() === "away"
                    ? "bg-green-900 border-green-500 ring-2 ring-green-400"
                    : "bg-gray-800 border-gray-700"
                } transition-all duration-300`}
              >
                <CardHeader className="text-center pb-2">
                  <CardTitle
                    className={`text-lg ${getHighestProbability() === "away" ? "text-green-300" : "text-white"}`}
                  >
                    Victoria Visitante
                  </CardTitle>
                  <p className="text-sm text-gray-400">{awayTeam}</p>
                </CardHeader>
                <CardContent className="text-center">
                  <div
                    className={`text-4xl font-bold ${
                      getHighestProbability() === "away" ? "text-green-400" : "text-red-400"
                    }`}
                  >
                    {results.awayWin}%
                  </div>
                  {getHighestProbability() === "away" && (
                    <p className="text-green-300 text-sm mt-2 font-semibold">Resultado más probable</p>
                  )}
                </CardContent>
              </Card>
            </div>

            <div className="text-center mt-8">
              <p className="text-gray-400 text-sm">
                * Las predicciones se basan en análisis estadístico y pueden no reflejar el resultado real del partido
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
