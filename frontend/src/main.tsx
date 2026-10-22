import React from 'react'
import ReactDOM from 'react-dom/client'
import { createHashRouter, RouterProvider } from 'react-router-dom'
import App from './App'
import { carregarMapa, instalarFetchPublico } from './api'
import Gate from './Gate'
import Dashboard from './pages/Dashboard'
import PatentPage from './pages/PatentPage'
import Patents from './pages/Patents'
import Runs from './pages/Runs'
import Roadmap from './pages/Roadmap'
import Docket from './pages/Docket'
import Compiler from './pages/Compiler'
import Pendencias from './pages/Pendencias'
import TglCore from './pages/TglCore'
import Fronteira from './pages/Fronteira'
import Custodia from './pages/Custodia'
import Epct from './pages/Epct'
import IaldNativa from './pages/IaldNativa'
import Classes from './pages/Classes'
import Users from './pages/Users'
import './styles.css'

const router = createHashRouter([
  {
    path: '/', element: <App />, children: [
      { index: true, element: <Dashboard /> },
      { path: 'classes', element: <Classes /> },
      { path: 'patents', element: <Patents /> },
      { path: 'patents/:id', element: <PatentPage /> },
      { path: 'runs', element: <Runs /> },
      { path: 'roadmap', element: <Roadmap /> },
      { path: 'docket', element: <Docket /> },
      { path: 'compiler', element: <Compiler /> },
      { path: 'pendencias', element: <Pendencias /> },
      { path: 'tgl-core', element: <TglCore /> },
      { path: 'fronteira', element: <Fronteira /> },
      { path: 'custodia', element: <Custodia /> },
      { path: 'epct', element: <Epct /> },
      { path: 'iald-nativa', element: <IaldNativa /> },
      { path: 'usuarios', element: <Users /> },
    ],
  },
])

// MODO PÚBLICO DE VISUALIZAÇÃO: o fetch passa pelo retrato e o mapa carrega antes de montar (no build normal, nada muda)
instalarFetchPublico()
carregarMapa().finally(() => ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Gate>
      <RouterProvider router={router} />
    </Gate>
  </React.StrictMode>,
))
