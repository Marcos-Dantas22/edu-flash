# 📚 EDU-FLASH

**Edu-Flash** é uma plataforma de aprendizado baseada em flashcards, projetada para oferecer uma experiência eficiente tanto para alunos autodidatas quanto para professores e seus alunos. O sistema permite criar, organizar e revisar conteúdos por meio de técnicas de aprendizado incremental e repetição espaçada.

---

## 🧠 Ideia Principal

O projeto combina os conceitos de:

- **Aprendizado Incremental**: introdução regular de novos conteúdos em pequenas quantidades.
- **Repetição Espaçada**: revisão dos conteúdos em intervalos otimizados com base no desempenho do usuário.
- **Gamificação**: o progresso é medido através de pontuações, precisão e status de memorização.

---

## 🎯 Objetivos do Sistema

1. **Ambiente Educacional para Professores**  
   Criar uma estrutura onde professores possam:
   - Criar grupos de flashcards por tema ou disciplina.
   - Compartilhar grupos com seus alunos.
   - Monitorar o progresso individual e coletivo.
   - Avaliar taxa de acerto, frequência de revisão e desempenho ao longo do tempo.

2. **Modo Autodidata**  
   Permitir que qualquer usuário possa:
   - Criar seus próprios grupos de estudo.
   - Gerenciar revisões e acompanhar seu próprio desempenho.
   - Receber recomendações de revisão baseadas na memória de longo prazo.

---

## 👥 Perfis de Usuário

- **Professor**
  - Criação de grupos de flashcards.
  - Atribuição de grupos a alunos.
  - Acompanhamento da performance dos alunos.
  - Visualização de relatórios de aprendizado.

- **Aluno**
  - Acesso a grupos compartilhados por professores.
  - Visualização da própria performance.
  - Participação em treinamentos e revisões.

- **Autodidata**
  - Criação e organização dos próprios flashcards.
  - Gerenciamento independente do aprendizado e revisões.

---

## 🧩 Tipos de Flashcards

- **Frente e Verso (clássico)**: termo e definição.
- **Múltipla Escolha**: seleção entre alternativas.
- **Escolha Correta (Choose)**: identificação de sentenças ou palavras corretas.

---

## 📈 Lógica de Pontuação e Revisão

Cada grupo de flashcards possui:

- **Taxa de Aprendizado**: medida de acerto ao longo das sessões.
- **Intervalo de Revisão Dinâmico**: adaptado com base na performance.
- **Critério de Memorização**:
  - Um grupo é considerado **memorizado** se o usuário mantém **mais de 90% de precisão por pelo menos 2 meses**.

---

## ⚙️ Instalação e Ambiente de Desenvolvimento

### Pré-requisitos

### Clone o repositório

```bash
git clone https://github.com/Marcos-Dantas22/edu-flash.git
cd edu-flash
