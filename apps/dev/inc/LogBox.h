/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        LogBox.h
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2023-12-24     xqyjlj       initial version
 */

#ifndef LOG_BOX_H
#define LOG_BOX_H

#include <QPlainTextEdit>

class LogBox final : public QPlainTextEdit
{
    Q_OBJECT
  public:
    explicit LogBox(QWidget *parent = nullptr);
    ~LogBox() override;

    void lineNumberAreaPaintEvent(const QPaintEvent *event) const;
    int lineNumberAreaWidth() const;

  public slots:
    void append(const QString &text);

  protected:
    void resizeEvent(QResizeEvent *event) override;

  private:
    class LineNumberArea final : public QWidget
    {
      public:
        explicit LineNumberArea(LogBox *editor)
            : QWidget(editor), codeEditor(editor)
        {
        }

        QSize sizeHint() const override
        {
            return { codeEditor->lineNumberAreaWidth(), 0 };
        }

      protected:
        void paintEvent(QPaintEvent *event) override
        {
            codeEditor->lineNumberAreaPaintEvent(event);
        }

      private:
        LogBox *codeEditor;
    };

  private slots:
    void updateLineNumberAreaWidth(int new_block_count);
    void updateLineNumberArea(const QRect &rect, int dy);

  private:
    QWidget *lineNumberArea_;
};

#endif /** LOG_BOX_H */
